import { FC, Fragment, ReactElement, useEffect, useRef, useState } from "react";
import {
  Accordion,
  AccordionHeader,
  AccordionBody,
} from "@material-tailwind/react";

const Example: FC<{ items: { heading: string; item: ReactElement }[] }> = ({
  items,
}) => {
  const [open, setOpen] = useState(0);

  const handleOpen = (value: number) => {
    setOpen(open === value ? 0 : value);
  };

  return (
    <Fragment>
      {items &&
        items.map((cat, i) => {
          const accordElem = useRef(null);
          return (
            <Accordion
              key={`${cat.heading}_${i}`}
              ref={accordElem}
              open={open === i + 1}
            >
              <AccordionHeader
                onClick={(_) => {
                  handleOpen(i + 1);
                  accordElem.current.scrollIntoView({
                    behavior: "smooth",
                    block: "end",
                    inline: "nearest",
                  });
                }}
              >
                {cat.heading}
              </AccordionHeader>
              <AccordionBody>{cat.item}</AccordionBody>
            </Accordion>
          );
        })}
    </Fragment>
  );
};

export default Example;
