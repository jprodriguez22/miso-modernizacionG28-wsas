import { apiDomain } from "../../../../app.config";

// Variable definition
const overpriceThreshold = 1.5;
const yieldCalculationThreshold = 0.7;

// Dataset functions
async function loadDataset() {
  try {
    const response = await fetch(`${apiDomain}/produccion/costos`, {
      method: "GET",
      mode: "cors", // Change 'no-cors' to 'cors' if the server allows cross-origin requests
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}

async function loadOrderDetailsByDefect(order) {
  try {
    const response = await fetch(`${apiDomain}/produccion/costos/defectos/${order}`, {
      method: "GET",
      mode: "cors", // Change 'no-cors' to 'cors' if the server allows cross-origin requests
    });
    const data = await response.json();

    if (response.status === 404) {
      return {}
    }

    // Transformation of the data into a single array
    const transformedData = {
      Cantidad: [],
      Costo: [],
      Defecto: [],
      Orden: [],
      Porcentaje: []
    };

    data.forEach(item => {
      transformedData.Cantidad.push(item.Cantidad)
      transformedData.Costo.push(Math.round(item.Costo*100)/100)
      transformedData.Defecto.push(item.Defecto)
      transformedData.Orden.push(item.Orden)
      transformedData.Porcentaje.push(Math.round(item.Porcentaje*100)/100)
    })

    return transformedData;

  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}

async function loadOrderDetailsByOrigin(order) {
  try {
    const response = await fetch(`${apiDomain}/produccion/costos/origenes/${order}`, {
      method: "GET",
      mode: "cors", // Change 'no-cors' to 'cors' if the server allows cross-origin requests
    });
    const data = await response.json();

    if (response.status === 404) {
      return {}
    }

    // Transformation of the data into a single array
    const transformedData = {
      Cantidad: [],
      Costo: [],
      Origen: [],
      Orden: [],
      Porcentaje: []
    };

    data.forEach(item => {
      transformedData.Cantidad.push(item.Cantidad)
      transformedData.Costo.push(Math.round(item.Costo*100)/100)
      transformedData.Origen.push(item.Origen)
      transformedData.Orden.push(item.Orden)
      transformedData.Porcentaje.push(Math.round(item.Porcentaje*100)/100)
    })
    
    return transformedData;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}

// Logic functions
function overpricedCount(dataset) {
  return dataset.filter((item) => item.RelacionSobrecosto >= overpriceThreshold)
    .length;
}

function calculateYield(dataset) {
  dataset = dataset.filter(
    (item) => item.RelacionSobrecosto >= yieldCalculationThreshold
  );
  const sumCostoPlan = dataset.reduce((acc, item) => acc + item.CostoPlan, 0);
  const sumCostoReal = dataset.reduce((acc, item) => acc + item.CostoReal, 0);
  return Math.round(
    (sumCostoPlan / (sumCostoReal + sumCostoReal * 0.22)) * 100
  );
}

function calculateExcessMoney(dataset) {
  dataset = dataset.filter(
    (item) => item.RelacionSobrecosto >= yieldCalculationThreshold
  );
  const sumCostoPlan = dataset.reduce((acc, item) => acc + item.CostoPlan, 0);
  const sumCostoReal = dataset.reduce((acc, item) => acc + item.CostoReal, 0);
  return Math.round((sumCostoReal - sumCostoPlan + sumCostoReal * 0.22));
}

function calculateOvercostRelation(dataset) {
  dataset = dataset.filter(
    (item) => item.RelacionSobrecosto >= yieldCalculationThreshold
  );
  const sumCostoPlan = dataset.reduce((acc, item) => acc + item.CostoPlan, 0);
  const sumCostoReal = dataset.reduce((acc, item) => acc + item.CostoReal, 0);
  return Math.round(((sumCostoReal + sumCostoReal * 0.22)/sumCostoPlan)*100)/100;
}

function countActiveOrders(dataset) {
  return dataset.length
}

// CSS Functions
function defineDivBackground(value) {
  if (value >= 80) {
    return 'green-background'
  }
  else if (value < 80 && value >= 70) {
    return 'yellow-background'
  }
  else if (value < 70) {
    return 'red-background'
  }
  else {
    return 'clear-background'
  }
}

export {
  loadDataset,
  loadOrderDetailsByOrigin,
  loadOrderDetailsByDefect,
  calculateYield,
  calculateExcessMoney,
  calculateOvercostRelation,
  countActiveOrders,
  overpricedCount,
  defineDivBackground
};
