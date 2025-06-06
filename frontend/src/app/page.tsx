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

  const [history, setHistory] = useState<ResultType[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/networth`);
      if (res.ok) {
        const data: ResultType[] = await res.json();
        setHistory(data);
      }
    };
    fetchData();
  }, []);

  const [result, setResult] = useState<ResultType | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    const updatedForm = { ...form, [name]: Number(value) || 0 };
    setForm(updatedForm);
    localStorage.setItem("financial_form", JSON.stringify(updatedForm));
  };
// page.tsx

  const handleSubmit = async () => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/networth`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    const data: ResultType = await res.json();
    setResult(data);

    // ✅ 이 줄을 추가하세요!
    // 새 계산 결과를 history 상태의 맨 뒤에 추가하여 목록을 바로 업데이트합니다.
    setHistory(prevHistory => [...prevHistory, data]);
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

  const chartData = getChartData();

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

      {chartData && (
        <div style={{ marginTop: 40 }}>
          <h3>📉 자산/부채 시각화</h3>
          <div style={{ maxWidth: 500 }}>
            <Bar data={chartData} />
          </div>
        </div>
      )}

      {history.length > 0 && (
        <div style={{ marginTop: 40 }}>
          <h3>📁 이전 순자산 기록</h3>
          <ul>
            {history.map((entry, idx) => (
              <li key={idx}>
                자산: {entry.total_assets.toLocaleString()} 원 / 부채: {entry.total_liabilities.toLocaleString()} 원 / 순자산: {entry.net_worth.toLocaleString()} 원
              </li>
            ))}
          </ul>
        </div>
      )}
    </main>
  );
}