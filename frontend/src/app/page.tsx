"use client";
import { useState } from "react";
import dummyData from "@/data";
import { toggleCategoryProductListChecked, selectMap } from "@/types";
import ProductList from "../components/ProductList";
import TotalPrice from "@/components/TotalPrice";
import Accordion from "@/components/Accordion";

export default function Home() {
  const data = dummyData;
  const [itemsChecked, setItemsChecked] = useState(selectMap(dummyData));

  const setProductSelectTrue = (catId: number, prodId: number) =>
    setItemsChecked(
      toggleCategoryProductListChecked(itemsChecked, catId, prodId)
    );

  return (
    <main className={""}>
      <TotalPrice
        products={data}
        itemsChecked={itemsChecked}
        toggleItem={setProductSelectTrue}
      />
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
    </main>
  );
}
