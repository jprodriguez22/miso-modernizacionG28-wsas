// Variable definition
const overpriceThreshold = 1.5;

function filterDataset(
    dataset,
    complex,
    market,
    block,
    level,
    formula,
    overprice,
    area,
    client,
    vehicles,
    order,
    zfer
  ) {
    if (complex !== "") {
      dataset = dataset.filter((item) => item.Complex === parseInt(complex));
    }
    if (!market.includes("")) {
      dataset = dataset.filter((item) => market.includes(item.Mercado));
    }
    if (!block.includes("")) {
      dataset = dataset.filter((item) => block.includes(item.Bloque));
    }
    if (!level.includes("")) {
      dataset = dataset.filter((item) => level.includes(item.Nivel));
    }
    if (!formula.includes("")) {
      dataset = dataset.filter((item) => formula.includes(item.Formula));
    }
    if (overprice !== "") {
      if (parseInt(overprice) === 1) {
        dataset = dataset.filter(
          (item) => item.RelacionSobrecosto >= overpriceThreshold
        );
      } else if (parseInt(overprice) === 0) {
        dataset = dataset.filter(
          (item) => item.RelacionSobrecosto < overpriceThreshold
        );
      }
    }
    if (!area.includes("")) {
      dataset = dataset.filter((item) => area.includes(item.Puestodetrabajo));
    }
    if (!client.includes("")) {
      dataset = dataset.filter((item) => client.includes(item.Cliente));
    }
    if (!vehicles.includes("")) {
      dataset = dataset.filter((item) => vehicles.includes(item.Vehiculo));
    }
    if (order > 0 || order !== '') {
      let stringOrder = String(order).replace(/\D/g, '')
      dataset = dataset.filter((item) => String(item.Orden).includes(stringOrder));
    }
    if (zfer > 0 || zfer !== '') {
      const stringZfer = String(zfer).replace(/\D/g, '')
      dataset = dataset.filter((item) => String(item.ZFER).includes(stringZfer));
    }
    return dataset;
  }

function sortTableBy(dataset, currentHeader, order) {
  return dataset = dataset.sort((a, b) => {
    const valueA = a[currentHeader];
    const valueB = b[currentHeader];

    if (order === 'ASCENDING') {
      if (valueA < valueB) {
        return -1;
      }
      else if (valueA > valueB) {
        return 1;
      }
      else {
        return 0;
      }
    }
    else {
      if (valueA < valueB) {
        return 1;
      }
      else if (valueA > valueB) {
        return -1;
      }
      else {
        return 0;
      }
    }
  });
}

function searchOnFilter(input, parameter, dataset) {
  const parameterList = dataset.map((item) => item[parameter]);
  var parameterUnique = [...new Set(parameterList)];
  parameterUnique = parameterUnique.sort((a, b) => a.localeCompare(b));
  if (!input || input == "" || input == 0) {
    return parameterUnique
  }
  return parameterUnique.filter((value) => value.toLowerCase().includes(input.toLowerCase()))
}

export {
  filterDataset,
  sortTableBy,
  searchOnFilter
};
