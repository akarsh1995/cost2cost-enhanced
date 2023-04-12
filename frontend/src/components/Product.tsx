import { Checkbox, Typography } from "@material-tailwind/react";
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
        <Checkbox
          className="h-7 w-7"
          type="checkbox"
          id={prodId}
          name={prodId}
          checked={isChecked}
          onChange={onToggle}
          label={
            <Typography variant={isChecked ? "h6" : "paragraph"}>
              {label}
            </Typography>
          }
        />
      </div>
    </div>
  );
};

export default Product;
