import { useEffect, useState } from 'react';

const YourComponent = () => {
  const [networthRecords, setNetworthRecords] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch("https://financial-web-backend.onrender.com/api/networth");
        const data = await res.json();
        setNetworthRecords(data);
      } catch (error) {
        console.error("Failed to fetch net worth data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h3>💾 저장된 순자산 기록</h3>
      <ul>
        {networthRecords.map((item, index) => (
          <li key={index}>
            총 자산: {item.total_assets} | 총 부채: {item.total_liabilities} | 순자산: {item.net_worth}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default YourComponent;