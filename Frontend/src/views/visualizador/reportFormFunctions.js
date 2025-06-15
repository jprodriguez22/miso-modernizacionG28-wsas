import { apiDomain } from "../../../app.config";

import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

async function loadReport(body) {
  try {
    const dataObject = JSON.stringify(body);
    const response = await fetch(
      `${apiDomain}/visualizador/reportes`,
      {
        method: "POST",
        mode: "cors",
        headers: { "Content-Type": "application/json; charset=ISO-8859-1" },
        body: dataObject,
      }
    );
    toast("Mensaje enviado correctamente", {
      "type": "success",
      "position": "bottom-right",
      "dangerouslyHTMLString": true,
    });
  } catch (error) {
    toast("No se ha podido enviar el reporte", {
      "type": "error",
      "position": "bottom-right",
      "dangerouslyHTMLString": true,
    })
    console.error("Error fetching data:", error);
    throw error;
  }
}

function populateProblemTypes(category) {
  let problemTypes = [];
  switch (category) {
    case "Fullkit":
      problemTypes = ["Aceros", "Artes", "Logos", "Mallas", "Moldes"];
      break;
    case "Producto":
      problemTypes = [
        "Archivos de corte",
        "Desarrollo errado",
        "Falta información en la OP",
        "Planos",
        "Posicionadores",
      ];
      break;
    case "LeccionesAprendidas":
      problemTypes = [
        "Lección incoherente",
        "No se muestra la imagen de la lección",
        "No se muestra el video de la lección",
      ];
  }
  return problemTypes;
}

export { loadReport, populateProblemTypes };
