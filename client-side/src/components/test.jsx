import { useState } from "react";

export default function App() {
  const [advice, setadvice] = useState("");
  const [count, setcount] = useState(0);

  async function getadvice() {
    const res = await fetch("http://127.0.0.1:5000/category");
    const data = await res.json();
    setadvice(data.categories[0].title);
    setcount((c) => c + 1);
    
  }

  return (
    <div>
      <h1>{advice}</h1>
      <button onClick={getadvice}>Get Advise</button>
      <Massage count={count} />
    </div>
  );
}

function Massage(props) {
  return (
    <p>
      you have read <strong>{props.count}</strong> pieces of advice
    </p>
  );
}
