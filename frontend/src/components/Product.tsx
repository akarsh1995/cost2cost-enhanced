import { FC } from "react";

const Product: FC<{
  onToggle: () => void;
  isChecked: boolean;
  prodId: string;
  label: string;
}> = ({ isChecked, prodId, onToggle, label }) => {
  const className = isChecked ? "text-slate-600" : "text-slate-400";
  return (
    <div key={prodId} className={className}>
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
        <label htmlFor={prodId}>{label}</label>
      </div>
    </div>
  );
};

export default Product;
