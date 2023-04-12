"use client";
import { useEffect, useState } from "react";
import { toggleCategoryProductListChecked, selectMap } from "@/types";
import ProductList from "../components/ProductList";
import TotalPrice from "@/components/TotalPrice";
import Accordion from "@/components/Accordion";
import DataType from "@/types";
import axios, { Axios } from "axios";

export default function Home() {
  const [data, setData] = useState({
    data: [],
  });

  const [itemsChecked, setItemsChecked] = useState(
    selectMap({
      data: [],
    })
  );

  useEffect(() => {
    axios
      .get(process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000")
      .then((response) => {
        setData(response.data);
        setItemsChecked(selectMap(response.data));
      });
  }, []);

  const setProductSelectTrue = (catId: number, prodId: number) =>
    setItemsChecked(
      toggleCategoryProductListChecked(itemsChecked, catId, prodId)
    );

  return data.data.length > 0 ? (
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
  ) : (
    <></>
  );
}
