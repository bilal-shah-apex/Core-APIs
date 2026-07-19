function createPieceRow(label = "P1", width = "10", height = "20", quantity = "1") {
  const tbody = document.getElementById("piece-rows");
  const row = document.createElement("tr");

  row.innerHTML = `
    <td><input type="text" value="${label}" class="piece-label" /></td>
    <td><input type="number" min="0.01" step="0.01" value="${width}" class="piece-width" /></td>
    <td><input type="number" min="0.01" step="0.01" value="${height}" class="piece-height" /></td>
    <td><input type="number" min="1" step="1" value="${quantity}" class="piece-quantity" /></td>
  `;

  tbody.appendChild(row);
}

function collectInput() {
  const sheetWidth = document.getElementById("sheet-width").value;
  const sheetHeight = document.getElementById("sheet-height").value;
  const sheetUnits = document.getElementById("sheet-units").value;
  const sheetType = document.getElementById("sheet-type").value;

  const pieceRows = document.querySelectorAll("#piece-rows tr");
  const cuttingPieces = [];

  pieceRows.forEach((row) => {
    const label = row.querySelector(".piece-label").value.trim() || "Piece";
    const width = row.querySelector(".piece-width").value;
    const height = row.querySelector(".piece-height").value;
    const quantity = row.querySelector(".piece-quantity").value;

    cuttingPieces.push({
      label,
      width: Number(width),
      height: Number(height),
      quantity: Number(quantity),
    });
  });

  return {
    sheet: {
      width: Number(sheetWidth),
      height: Number(sheetHeight),
      units: sheetUnits,
      type: sheetType,
    },
    cutting_pieces: cuttingPieces,
  };
}

function showError(message) {
  const errorElement = document.getElementById("error-message");
  errorElement.textContent = message;
}

function showResult(result) {
  const jsonOutput = document.getElementById("json-output");
  jsonOutput.textContent = JSON.stringify(result, null, 2);

  const diagramFrame = document.getElementById("diagram-frame");
  diagramFrame.srcdoc = result.html_diagram || "<p>No diagram available.</p>";
}

function clearErrors() {
  showError("");
}

async function submitOptimization() {
  clearErrors();

  const payload = collectInput();

  try {
    const response = await fetch("/api/optimize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const result = await response.json();
    if (!response.ok) {
      showError(result.detail || "Request failed.");
      return;
    }

    showResult(result);
  } catch (error) {
    showError(error.message || "Network error.");
  }
}

function addPieceRow() {
  const rowCount = document.querySelectorAll("#piece-rows tr").length;
  createPieceRow(`P${rowCount + 1}`, "10", "20", "1");
}

function removePieceRow() {
  const tbody = document.getElementById("piece-rows");
  if (tbody.children.length > 1) {
    tbody.removeChild(tbody.lastElementChild);
  }
}

function initialize() {
  const addButton = document.getElementById("add-piece");
  const removeButton = document.getElementById("remove-piece");
  const submitButton = document.getElementById("submit-button");

  addButton.addEventListener("click", addPieceRow);
  removeButton.addEventListener("click", removePieceRow);
  submitButton.addEventListener("click", submitOptimization);

  createPieceRow("P1", "10", "20", "1");
  createPieceRow("P2", "12", "18", "3");
}

document.addEventListener("DOMContentLoaded", initialize);
