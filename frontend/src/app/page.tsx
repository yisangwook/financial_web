"use client";

import { useState, useEffect } from "react";
import type { ChartData } from "chart.js";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function Home() {
  const [form, setForm] = useState({
    cash: 0,
    stock: 0,
    savings: 0,
    real_estate: 0,
    loan: 0,
    credit_card: 0,
    jeonse: 0,
  });

  useEffect(() => {
    const saved = localStorage.getItem("financial_form");
    if (saved) {
      setForm(JSON.parse(saved));
    }
  }, []);

  type ResultType = {
    total_assets: number;
    total_liabilities: number;
    net_worth: number;
  };

  const [result, setResult] = useState<ResultType | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    const updatedForm = { ...form, [name]: Number(value) || 0 };
    setForm(updatedForm);
    localStorage.setItem("financial_form", JSON.stringify(updatedForm));
  };

  const handleSubmit = async () => {
    const res = await fetch("http://127.0.0.1:8000/api/networth", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    const data: ResultType = await res.json();
    setResult(data);
  };

  const getChartData = (): ChartData<"bar"> | null => {
    if (!result) return null;

    return {
      labels: ["총 자산", "총 부채", "순자산"],
      datasets: [
        {
          label: "재무 상태",
          data: [result.total_assets, result.total_liabilities, result.net_worth],
          backgroundColor: ["#4caf50", "#f44336", "#2196f3"],
        },
      ],
    };
  };

  return (
    <main style={{ padding: 40 }}>
      <h1>📊 Net Worth Calculator</h1>

      <h2>🟢 자산</h2>
      <div>
        <label>현금:</label>
        <input type="number" name="cash" value={form.cash} onChange={handleChange} />
      </div>
      <div>
        <label>주식:</label>
        <input type="number" name="stock" value={form.stock} onChange={handleChange} />
      </div>
      <div>
        <label>예금:</label>
        <input type="number" name="savings" value={form.savings} onChange={handleChange} />
      </div>
      <div>
        <label>부동산:</label>
        <input type="number" name="real_estate" value={form.real_estate} onChange={handleChange} />
      </div>

      <h2>🔴 부채</h2>
      <div>
        <label>대출:</label>
        <input type="number" name="loan" value={form.loan} onChange={handleChange} />
      </div>
      <div>
        <label>신용카드:</label>
        <input type="number" name="credit_card" value={form.credit_card} onChange={handleChange} />
      </div>
      <div>
        <label>전세보증금:</label>
        <input type="number" name="jeonse" value={form.jeonse} onChange={handleChange} />
      </div>

      <button onClick={handleSubmit} style={{ marginTop: 20 }}>
        계산하기
      </button>

      {result && (
        <div style={{ marginTop: 30 }}>
          <h2>✅ 결과</h2>
          <p>총 자산: {result.total_assets.toLocaleString()} 원</p>
          <p>총 부채: {result.total_liabilities.toLocaleString()} 원</p>
          <p>순자산: {result.net_worth.toLocaleString()} 원</p>
        </div>
      )}

      {result && (
        <div style={{ marginTop: 40 }}>
          <h3>📉 자산/부채 시각화</h3>
          <div style={{ maxWidth: 500 }}>
            <Bar data={getChartData()} />
          </div>
        </div>
      )}
    </main>
  );
}