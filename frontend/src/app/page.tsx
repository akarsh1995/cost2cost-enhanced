"use client";
import { FC, useEffect, useState } from "react";
import {
  toggleCategoryProductListChecked,
  selectMap,
  SelectMapType,
} from "@/types";
import ProductList from "../components/ProductList";
import TotalPrice from "@/components/TotalPrice";
import Accordion from "@/components/Accordion";
import DataType from "@/types";
import axios from "axios";
import SimpleFooter from "@/components/Footer";

const Main: FC<{ productData: DataType }> = ({ productData }) => {
  const data = productData;
  const [itemsChecked, setItemsChecked]: [
    itemsChecked: SelectMapType,
    setItemsChecked: (data: SelectMapType) => void
  ] = useState(selectMap(productData));

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

export default function Home() {
  const [productData, setproductData] = useState({ data: [] });

  useEffect(() => {
    axios
      .get(process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000")
      .then(({ data }) => {
        setproductData(data);
      });
  }, []);

  return (
    <>
      {productData.data.length === 0 ? (
        <div className="w-screen h-screen flex flex-col items-center justify-between">
          <div className="flex justify-center items-center h-full">
            <div
              className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"
              role="status"
            ></div>
          </div>
          <SimpleFooter />
        </div>
      ) : (
        <Main productData={productData} />
      )}
    </>
  );
}
