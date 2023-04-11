interface ProductType {
  id: number;
  name: string;
  price: number;
}

interface CategoryType {
  category: string;
  gst: number;
  products: ProductType[];
}

interface DataType {
  data: CategoryType[];
}

interface SelectMapType {
  data: {
    category: string;
    gst: number;
    products: boolean[];
  }[];
}

const selectMap: (data: DataType) => SelectMapType = (data: DataType) => {
  return {
    data: data.data.map((category) => {
      return {
        ...category,
        products: category.products.map((_) => false),
      };
    }),
  };
};

const filterDataFromMap: (data: DataType, mapp: SelectMapType) => DataType = (
  data,
  mapp
) => {
  return {
    data: mapp.data.map((catMapData, catId) => {
      return {
        ...catMapData,
        products: data.data[catId].products.filter(
          (_, pid) => catMapData.products[pid]
        ),
      };
    }),
  };
};

const toggleCategoryProductListChecked = (
  itemsChecked: SelectMapType,
  catId: number,
  productId: number
) => {
  const newItemsChecked: SelectMapType = {
    data: [
      ...itemsChecked.data.slice(0, catId),
      {
        ...itemsChecked.data[catId],
        products: [
          ...itemsChecked.data[catId].products.slice(0, productId),
          !itemsChecked.data[catId].products[productId],
          ...itemsChecked.data[catId].products.slice(
            productId + 1,
            itemsChecked.data[catId].products.length
          ),
        ],
      },
      ...itemsChecked.data.slice(catId + 1, itemsChecked.data.length),
    ],
  };
  return newItemsChecked;
};

export default DataType;
export { selectMap, filterDataFromMap, toggleCategoryProductListChecked };
export type { CategoryType, ProductType, SelectMapType };
