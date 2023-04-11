const sum = (arr: number[]) => {
  var s = 0;
  arr.forEach((price) => {
    s += price;
  });
  return s;
};

export { sum };
