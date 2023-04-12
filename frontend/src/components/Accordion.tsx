import { FC, Fragment, ReactElement, useRef, useState } from "react";
import {
  Accordion,
  AccordionHeader,
  AccordionBody,
} from "@material-tailwind/react";

interface PP {
  heading: string;
  item: ReactElement;
}

interface SS {
  items: PP[];
}

const Accord: FC<{ cat: PP; isActive: boolean; handleOpen: () => void }> = ({
  cat,
  isActive,
  handleOpen,
}) => {
  const accordElem = useRef<HTMLDivElement>(null);
  return (
    <Accordion ref={accordElem} open={isActive}>
      <AccordionHeader
        onClick={(_) => {
          handleOpen();
          if (accordElem.current) {
            accordElem.current.scrollIntoView({
              behavior: "smooth",
              block: "end",
              inline: "nearest",
            });
          }
        }}
      >
        {cat.heading}
      </AccordionHeader>
      <AccordionBody>{cat.item}</AccordionBody>
    </Accordion>
  );
};

const Example: FC<SS> = ({ items }) => {
  const [open, setOpen] = useState(0);

  const handleOpen = (value: number) => {
    setOpen(open === value ? 0 : value);
  };

  return (
    <Fragment>
      {items &&
        items.map((cat, i) => {
          return (
            <Accord
              key={`${cat.heading}_${i}`}
              cat={cat}
              isActive={open === i + 1}
              handleOpen={() => handleOpen(i + 1)}
            />
          );
        })}
    </Fragment>
  );
};

export default Example;
