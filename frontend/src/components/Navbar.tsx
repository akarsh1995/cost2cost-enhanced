import { IconButton, Typography } from "@material-tailwind/react";
import { FC, ReactNode } from "react";

const CloseSVG = () => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      className="h-6 w-6"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M6 18L18 6M6 6l12 12"
      />
    </svg>
  );
};

const HamburgerSVG = () => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      className="h-6 w-6"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M4 6h16M4 12h16M4 18h16"
      />
    </svg>
  );
};

const NavListItem: FC<{ children: ReactNode }> = ({ children }) => {
  return (
    <Typography
      as="li"
      variant="small"
      color="blue-gray"
      className="p-1 font-normal"
    >
      {children}
    </Typography>
  );
};

const NavbarIconButton: FC<{
  setOpenNav: (toOpen: boolean) => void;
  openNav: boolean;
}> = ({ setOpenNav, openNav }) => {
  return (
    <IconButton
      variant="text"
      className="ml-auto h-6 w-6 text-inherit hover:bg-transparent focus:bg-transparent active:bg-transparent lg:hidden"
      ripple={false}
      onClick={() => setOpenNav(!openNav)}
    >
      {openNav ? <CloseSVG /> : <HamburgerSVG />}
    </IconButton>
  );
};

export { NavListItem, NavbarIconButton };
