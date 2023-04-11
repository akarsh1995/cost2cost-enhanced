"use client";
import { Inter } from "next/font/google";
import { useState } from "react";
import dummyData from "@/data";
import DataType, {
  toggleCategoryProductListChecked,
  filterDataFromMap,
  selectMap,
} from "@/types";
import ProductList from "../components/ProductList";
import TotalPrice from "@/components/TotalPrice";
import Accordion from "@/components/Accordion";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const data = dummyData;
  const [itemsChecked, setItemsChecked] = useState(selectMap(dummyData));

  const setProductSelectTrue = (catId: number, prodId: number) =>
    setItemsChecked(
      toggleCategoryProductListChecked(itemsChecked, catId, prodId)
    );

  return (
    <main className={""}>
      <div className="sticky z-30 top-0 p-5 min-h-48 backdrop-blur-sm">
        <TotalPrice
          products={data}
          itemsChecked={itemsChecked}
          toggleItem={setProductSelectTrue}
        />
      </div>
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
