import React, { FC, ReactNode, useCallback, useRef, useState } from "react";
import { toPng, toSvg } from "html-to-image";
import { Button } from "@material-tailwind/react";

const DownloadIcon: FC<{ className: string }> = ({ className }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    className={className}
    viewBox="0 0 24 24"
    fill="none"
  >
    <path
      d="M12 12V19M12 19L9.75 16.6667M12 19L14.25 16.6667M6.6 17.8333C4.61178 17.8333 3 16.1917 3 14.1667C3 12.498 4.09438 11.0897 5.59198 10.6457C5.65562 10.6268 5.7 10.5675 5.7 10.5C5.7 7.46243 8.11766 5 11.1 5C14.0823 5 16.5 7.46243 16.5 10.5C16.5 10.5582 16.5536 10.6014 16.6094 10.5887C16.8638 10.5306 17.1284 10.5 17.4 10.5C19.3882 10.5 21 12.1416 21 14.1667C21 16.1917 19.3882 17.8333 17.4 17.8333"
      strokeWidth={2}
      stroke="white"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

const Imagify: React.FC<{ children: ReactNode }> = ({ children }) => {
  const ref = useRef<HTMLDivElement>(null);

  const onButtonClick = useCallback(() => {
    if (ref.current === null) {
      return;
    }

    toPng(ref.current, { cacheBust: true })
      .then((dataUrl) => {
        const link = document.createElement("a");
        link.download = "productsSelected.png";
        link.href = dataUrl;
        link.click();
      })
      .catch((err) => {
        console.log(err);
      });
  }, [ref]);
  const [hideModal, setHideModal] = useState(true);
  const onShowModal = () => setHideModal(false);
  const onHideModal = () => setHideModal(true);

  return (
    <>
      <div className="z-50 absolute top-0 left-0" hidden={hideModal} ref={ref}>
        {children}
      </div>
      <Button
        className="flex items-center"
        onMouseEnter={onShowModal}
        onMouseLeave={onHideModal}
        onClick={onButtonClick}
      >
        <DownloadIcon className="mr-2 block w-6 h-6" />
        LIST
      </Button>
    </>
  );
};

export default Imagify;
