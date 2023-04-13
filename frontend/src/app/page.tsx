import Main from "@/components/Main";

async function getProductData() {
  const res = await fetch(
    process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000",
    { next: { revalidate: 3600 } }
  );
  return await res.json();
}

const Home = async () => {
  const productData = await getProductData();
  return <Main productData={productData} />;
};

export default Home;
