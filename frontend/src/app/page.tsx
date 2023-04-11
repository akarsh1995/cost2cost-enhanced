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

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const data = dummyData;
  const [itemsChecked, setItemsChecked] = useState(selectMap(dummyData));

  const setProductSelectTrue = (catId: number, prodId: number) =>
    setItemsChecked(
      toggleCategoryProductListChecked(itemsChecked, catId, prodId)
    );

  return (
    <main className={inter.className}>
      {/* <main> */}
      <div className="sticky top-0 bg-white p-5 min-h-48">
        <TotalPrice
          products={data}
          itemsChecked={itemsChecked}
          toggleItem={setProductSelectTrue}
        />
      </div>
      <div className="p-5 md:p-10 space-y-10">
        {data.data.map((catData, catId) => {
          return (
            <div key={`${catId}_${catData.category}`}>
              <h2 className="text-2xl">{catData.category}</h2>
              <br />
              <ProductList
                selectedProductsMask={itemsChecked.data[catId].products}
                setItemsChecked={(productId: number) =>
                  setProductSelectTrue(catId, productId)
                }
                categoryData={catData}
              />
            </div>
          );
        })}
      </div>
    </main>
  );
}
