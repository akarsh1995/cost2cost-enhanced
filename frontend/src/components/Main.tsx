"use client";
import { FC, useState } from "react";
import DataType, {
  toggleCategoryProductListChecked,
  selectMap,
  SelectMapType,
} from "@/types";
import ProductList from "../components/ProductList";
import TotalPrice from "@/components/TotalPrice";
import Accordion from "@/components/Accordion";
import SimpleFooter from "@/components/Footer";

const Main: FC<{ productData: DataType }> = ({ productData: data }) => {
  const [itemsChecked, setItemsChecked]: [
    itemsChecked: SelectMapType,
    setItemsChecked: (data: SelectMapType) => void
  ] = useState(selectMap(data));

  const setProductSelectTrue = (catId: number, prodId: number) =>
    setItemsChecked(
      toggleCategoryProductListChecked(itemsChecked, catId, prodId)
    );

  return data.data.length > 0 ? (
    <>
      <main>
        <TotalPrice
          products={data}
          itemsChecked={itemsChecked}
          toggleItem={setProductSelectTrue}
        />
        <div className="p-5">
          <Accordion
            items={data.data.map((catData, catId) => {
              return {
                heading: catData.category,
                item: (
                  <div key={`${catId}_${catData.category}`}>
                    <ProductList
                      selectedProductsMask={itemsChecked.data[catId].products}
                      setItemsChecked={(productId: number) =>
                        setProductSelectTrue(catId, productId)
                      }
                      categoryData={catData}
                    />
                  </div>
                ),
              };
            })}
          />
        </div>
      </main>
      <SimpleFooter />
    </>
  ) : (
    <></>
  );
};

export default Main;
