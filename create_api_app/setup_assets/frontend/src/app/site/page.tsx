import Image from "next/image";

export default function Home() {
  return (
    <main className="">
      <section className="h-full w-full pt-36 relative flex items-center justify-center flex-col">
        {/* grid */}
        <div className="absolute bottom-0 left-0 right-0 top-0 bg-[linear-gradient(to_right,#161616_1px,transparent_1px),linear-gradient(to_bottom,#161616_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_110%)]"/>

        <p className="text-center">Project Template</p>
        <div></div>
      </section>
    </main>
  );
}
