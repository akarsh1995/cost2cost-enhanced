import { FC } from "react";
import DataType, { SelectMapType, filterDataFromMap } from "@/types";
import data from "@/data";

const fetchStatus = (catId: number, prodId: number, data: SelectMapType) => {
  return data.data[catId].products[prodId];
};

const hasZeroPriceData = (data: DataType, selectedMask: SelectMapType) => {
  for (let index = 0; index < selectedMask.data.length; index++) {
    const category = selectedMask.data[index];
    for (let pi = 0; pi < category.products.length; pi++) {
      const productIsSelected = category.products[pi];
      if (productIsSelected && data.data[index].products[pi].price == 0) {
        return true;
      }
    }
  }
  return false;
};

const TotalPrice: FC<{
  products: DataType;
  itemsChecked: SelectMapType;
  toggleItem: (catId: number, prodId: number) => void;
}> = ({ products, toggleItem, itemsChecked }) => {
  var s = 0;

  const anyDataZeroPriceSelected = hasZeroPriceData(products, itemsChecked);
  const filteredProducts: DataType = filterDataFromMap(products, itemsChecked);
  filteredProducts.data.forEach((c) =>
    c.products.forEach((p) => (s += p.price * (1 + c.gst / 100)))
  );

  return (
    <div className="space-y-6">
      <div>
        Total with GST: <span className="font-bold">{s.toFixed(2)}</span>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-3 auto-rows-fr">
        {products.data.map((c, catId) => {
          return c.products.map((p, pId) => {
            const key = `${c.category}${pId}`;
            const isChecked = fetchStatus(catId, pId, itemsChecked);
            const isPriceZero = data.data[catId].products[pId].price == 0;
            return (
              isChecked && (
                <div className="flex items-center">
                  <input
                    className="w-4 h-4"
                    key={key}
                    type="checkbox"
                    checked={isChecked}
                    id={key}
                    name={key}
                    onClick={() => toggleItem(catId, pId)}
                  />
                  &nbsp;
                  <label
                    className={isPriceZero ? "text-slate-400" : ""}
                    htmlFor={key}
                  >
                    {p.name}
                  </label>
                  {isPriceZero && <sup className="text-slate-400">*</sup>}
                </div>
              )
            );
          });
        })}
      </div>
      {anyDataZeroPriceSelected && (
        <div className="text-slate-400 text-right">
          * Ask the price on store
        </div>
      )}
    </div>
  );
};

export default TotalPrice;
