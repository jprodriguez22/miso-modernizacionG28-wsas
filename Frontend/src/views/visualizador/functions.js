import { apiDomain } from "../../../app.config";

async function actualizarPlanos() {
  try {
    const response = await fetch(
      `${apiDomain}/visualizador`,
      {
        method: "GET",
        mode: "cors", // Change 'no-cors' to 'cors' if the server allows cross-origin requests
      }
    );
    const data = await response.json();
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}

async function cargarInfoOrden(orden) {
  try {
    const response = await fetch(
      `${apiDomain}/visualizador/${orden}`,
      {
        method: "GET",
        mode: "cors", // Change 'no-cors' to 'cors' if the server allows cross-origin requests
      }
    );
    if (response.status === 404) {
      return null;
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}

async function cargarPlanoOrden(orden) {
  try {
    const response = await fetch(
      `${apiDomain}/visualizador/${orden}/plano`,
      {
        method: "GET",
        mode: "cors", // Change 'no-cors' to 'cors' if the server allows cross-origin requests
      }
    );
    const imagen = await response.blob();
    return imagen;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}

async function cargarCaracteristicasOrden(orden) {
  try {
    const response = await fetch(
      `${
        apiDomain
      }/visualizador/lecciones/caracteristicas/${orden}`,
      {
        method: "GET",
        mode: "cors", // Change 'no-cors' to 'cors' if the server allows cross-origin requests
      }
    );

    let data = await response.json();

    data = Object.fromEntries(
      Object.entries(data[0]).filter(([key, value]) => value > 0)
    );

    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}

async function actualizarLecciones() {
  try {
    const response = await fetch(
      `${apiDomain}/visualizador/lecciones/actualizar`,
      {
        method: "GET",
        mode: "cors", // Change 'no-cors' to 'cors' if the server allows cross-origin requests
      }
    );
    const data = await response.json();
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}

async function cargarLeccionesAprendidas(
  puesto_trabajo,
  caracteristicas,
  zfer
) {
  let charsArray = "";
  let charsCopy = { ...caracteristicas }
  charsCopy.Bomba = "Bomba"
  charsCopy.Curvatura = "Curvatura"
  charsCopy.Geometria = "Geometria"
  charsCopy.Logo = "Logo"
  if (charsCopy) {
    const objectChars = Object.keys(charsCopy);
    charsArray = objectChars.join(",");
  }
  try {
    let dataObject = JSON.stringify({
      puesto_trabajo: puesto_trabajo,
      caracteristicas: charsArray.toString(),
      zfer: zfer,
    });
    console.log(dataObject)
    const response = await fetch(
      `${apiDomain}/visualizador/lecciones/consultar`,
      {
        method: "POST",
        mode: "cors", // Change 'no-cors' to 'cors' if the server allows cross-origin requests
        headers: { "Content-Type": "application/json; charset=ISO-8859-1" },
        body: dataObject,
      }
    );
    const data = await response.json();
    console.log(data)
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}

async function cargarImagenLeccion(id) {
  try {
    const response = await fetch(
      `${
        apiDomain
      }/visualizador/lecciones/imagen?id=${id}`,
      {
        method: "GET",
        mode: "cors", // Change 'no-cors' to 'cors' if the server allows cross-origin requests
      }
    );
    if (response.status !== 200) {
      return null; // Return null if there's no image in the server
    }
    const imagen = await response.blob();
    return imagen;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}

function asignarImagenALeccion(lecciones) {
  lecciones.forEach(async (entry) => {
    entry["Imagen"] = await cargarImagenLeccion(entry.ID);
    if (entry["Imagen"]) {
      entry["Imagen"] = URL.createObjectURL(entry["Imagen"]);
    }
  });
  return lecciones;
}

function sortData(data) {
  const sortedKeys = Object.keys(data).sort();
  const sortedData = {};
  sortedKeys.forEach((key) => {
    sortedData[key] = data[key];
  });
  return sortedData;
}

const differentials_map = {
  "": "",
  Geometria: "Geometría",
  Logo: "Logo",
  Curvatura: "Curvatura",
  Bomba: "Bomba",
  Aluminum: "Cristal aluminum",
  GrisDark: "Cristal Gris Dark",
  GrisLight: "Cristal Gris Light",
  Tec: "Cristal TEC",
  White: "Cristal White",
  PUModAlto: "PU Mód. Alto",
  PUModMedio: "PU Mód. Medio",
  PUModBajo: "PU Mód. Bajo",
  PVBGris: "PVB Gris",
  Tejido: "PVB Tejido",
  CPET: "CPET(AL)",
  XIR: "XIR",
  Acero: "Acero",
  TNT: "Malla TNT",
  TNTFlex: "Malla TNT Flex",
  BandaNegraInterna: "Banda Negra Interna",
  Caja: "Caja",
  Chaflan: "Chaflan",
  Perforaciones: "Perforación",
  Encapsulado: "Encapsulado",
  TempladoQuimico: "Templado Químico",
  TermpladoTermico: "Templado Térmico",
};

export {
  actualizarPlanos,
  cargarInfoOrden,
  cargarPlanoOrden,
  cargarCaracteristicasOrden,
  actualizarLecciones,
  cargarLeccionesAprendidas,
  sortData,
  asignarImagenALeccion,
  differentials_map,
};
