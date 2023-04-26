import Main from "@/components/Main";

async function getProductData() {
  const res = await fetch(
    process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000",
    { next: { revalidate: 3600 } }
  );
  return await res.json();
}

export const metadata = {
  title: "COST TO COST PRICELIST PDF | with GST",
  description:
    "The only pricelist to build the best pc from Nehru Place COST TO COST. Calculate the price with GST to build",
  keywords: ["cost to cost", "cost2cost", "pdf", "gst", "Nehru Place"],
};

const Home = async () => {
  const productData = await getProductData();
  return <Main productData={productData} />;
};

export default Home;
