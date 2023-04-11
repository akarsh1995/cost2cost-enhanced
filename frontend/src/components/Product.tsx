import { Typography } from "@material-tailwind/react";
import { FC } from "react";

const Product: FC<{
  onToggle: () => void;
  isChecked: boolean;
  prodId: string;
  label: string;
}> = ({ isChecked, prodId, onToggle, label }) => {
  return (
    <div key={prodId}>
      <div className="flex items-center">
        <input
          className="h-7 w-7"
          type="checkbox"
          id={prodId}
          name={prodId}
          checked={isChecked}
          onChange={onToggle}
        />{" "}
        &nbsp; &nbsp;
        <label htmlFor={prodId}>
          <Typography variant={isChecked ? "h6" : "paragraph"}>
            {label}
          </Typography>
        </label>
      </div>
    </div>
  );
};

export default Product;
