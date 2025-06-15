import { apiDomain } from "../../../../app.config";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

async function cargarFNP(body) {
  try {
    const response = await fetch(
      //`${apiDomain}/fnp`,
      `http://localhost:5006/api/fnp`,
      {
        method: "POST",
        mode: "cors", // Change 'no-cors' to 'cors' if the server allows cross-origin requests
        headers: { "Content-Type": "application/json; charset=ISO-8859-1" },
        body: body,
      }
    );
    const data = await response.text()
    toast("Creación exitosa", {
        "type": "success",
        "position": "bottom-right",
        "dangerouslyHTMLString": true,
    })
    return data
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}

async function cargarListaFNP() {
  try {
    const response = await fetch(
      //`${apiDomain}/fnp`,
      `http://localhost:5006/api/fnp`,
      {
        method: "GET",
        mode: "cors", // Change 'no-cors' to 'cors' if the server allows cross-origin requests
      }
    );
    const data = JSON.parse(await response.json());
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}

export { cargarFNP, cargarListaFNP };
