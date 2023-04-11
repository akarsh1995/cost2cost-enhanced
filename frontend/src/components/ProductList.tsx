import { FC } from "react";
import { CategoryType } from "@/types";
import Product from "./Product";

const ProductList: FC<{
  selectedProductsMask: boolean[];
  setItemsChecked: (productId: number) => void;
  categoryData: CategoryType;
}> = ({ selectedProductsMask, setItemsChecked, categoryData }) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
      {categoryData.products.map((prod, i) => {
        const isChecked = selectedProductsMask[i];
        const id = `${categoryData.category}${i}`;
        return (
          <Product
            key={id}
            onToggle={() => setItemsChecked(i)}
            isChecked={isChecked}
            prodId={id}
            label={`${prod.name}`}
          />
        );
      })}
    </div>
  );
};

export default ProductList;
