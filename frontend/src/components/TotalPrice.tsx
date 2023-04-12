import React, { FC, ReactNode } from "react";
import DataType, { SelectMapType, filterDataFromMap } from "@/types";
import data from "@/data";
import {
  Navbar,
  Checkbox,
  Typography,
  MobileNav,
} from "@material-tailwind/react";

import { NavListItem, NavbarIconButton } from "./Navbar";

const Cb: FC<{
  id: string;
  isChecked: boolean;
  catId: number;
  pId: number;
  name: string;
  isPriceZero: boolean;
  toggleItem: (catId: number, pId: number) => void;
}> = ({ id, isChecked, catId, pId, name, isPriceZero, toggleItem }) => {
  return (
    <Checkbox
      id={id}
      name={id}
      checked={isChecked}
      onChange={() => toggleItem(catId, pId)}
      label={
        <div className="flex">
          {name}
          {isPriceZero && (
            <sup>
              <Typography variant="h6">*</Typography>
            </sup>
          )}{" "}
        </div>
      }
    />
  );
};

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
  const [openNav, setOpenNav] = React.useState(false);
  React.useEffect(() => {
    window.addEventListener(
      "resize",
      () => window.innerWidth >= 960 && setOpenNav(false)
    );
  }, []);

  const prods_ = products.data.map((c, catId) => {
    return c.products.map((p, pId) => {
      const key = `${c.category}${pId}`;
      const isChecked = fetchStatus(catId, pId, itemsChecked);
      const isPriceZero = data.data[catId].products[pId].price == 0;
      return isChecked ? (
        <NavListItem key={key}>
          <div className="flex items-center">
            <Cb
              id={key}
              isChecked={isChecked}
              catId={catId}
              pId={pId}
              name={p.name}
              isPriceZero={isPriceZero}
              toggleItem={toggleItem}
            />
          </div>
        </NavListItem>
      ) : (
        <React.Fragment key={key}></React.Fragment>
      );
    });
  });

  const NavList = () => (
    <ul className="mb-4 mt-2 grid grid-cols-4 gap-2 lg:mb-0 lg:mt-0 lg:items-center">
      {prods_}
    </ul>
  );

  const AskPriceMark = () =>
    anyDataZeroPriceSelected ? (
      <div className="flex justify-end">
        <Typography variant="h6" color="blue-gray">
          * Ask the price on store. Not included in total
        </Typography>
      </div>
    ) : (
      <></>
    );

  var s = 0;

  const anyDataZeroPriceSelected = hasZeroPriceData(products, itemsChecked);
  const filteredProducts: DataType = filterDataFromMap(products, itemsChecked);
  filteredProducts.data.forEach((c) =>
    c.products.forEach((p) => (s += p.price * (1 + c.gst / 100)))
  );

  return (
    <Navbar className="sticky inset-0 z-10 h-max max-w-full rounded-none py-2 px-4 lg:px-8 lg:py-4">
      <div className="flex items-center justify-between text-blue-gray-900">
        <div className="flex">
          <Typography className="mr-4 cursor-pointer py-1.5 font-medium">
            Total with GST:
          </Typography>
          <Typography variant="h4">{s.toFixed(2)}</Typography>
        </div>
        <div className="flex items-center gap-4">
          <div className="mr-4 hidden lg:block">
            <NavList />
            <AskPriceMark />
          </div>
          <NavbarIconButton setOpenNav={setOpenNav} openNav={openNav} />
        </div>
      </div>

      <MobileNav open={openNav}>
        <NavList />
        <AskPriceMark />
      </MobileNav>
    </Navbar>
  );
};

export default TotalPrice;
