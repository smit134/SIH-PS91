"use client";

import React from 'react';
import { PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer } from 'recharts';

const costData = [
  { name: 'Equipment', value: 80000 },
  { name: 'Working Capital', value: 30000 },
  { name: 'Marketing', value: 10000 },
  { name: 'Setup', value: 20000 },
];
const COLORS = ['#0d9488', '#3b82f6', '#f59e0b', '#8b5cf6'];

const cashFlowData = [
  { month: 'M1', revenue: 20000, expenses: 52000 },
  { month: 'M2', revenue: 35000, expenses: 40000 },
  { month: 'M3', revenue: 50000, expenses: 38000 },
  { month: 'M4', revenue: 60000, expenses: 40000 },
  { month: 'M5', revenue: 70000, expenses: 42000 },
  { month: 'M6', revenue: 75000, expenses: 45000 },
];

export function CostBreakdownChart() {
  return (
    <div className="w-full h-80 bg-white p-4 rounded-xl shadow-sm border border-slate-100 flex flex-col">
      <h3 className="text-lg font-semibold text-slate-800 mb-2">Cost Breakdown</h3>
      <div className="flex-1 min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={costData}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              fill="#8884d8"
              paddingAngle={5}
              dataKey="value"
            >
              {costData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <RechartsTooltip formatter={(value) => `₹${value.toLocaleString()}`} />
            <Legend verticalAlign="bottom" height={36}/>
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export function CashFlowChart() {
  return (
    <div className="w-full h-80 bg-white p-4 rounded-xl shadow-sm border border-slate-100 flex flex-col">
      <h3 className="text-lg font-semibold text-slate-800 mb-2">Monthly Cash Flow</h3>
      <div className="flex-1 min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={cashFlowData}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
            <XAxis dataKey="month" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
            <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `₹${value/1000}k`} />
            <RechartsTooltip 
              formatter={(value: number) => `₹${value.toLocaleString()}`}
              contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            />
            <Legend />
            <Line type="monotone" dataKey="revenue" name="Revenue" stroke="#0d9488" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
            <Line type="monotone" dataKey="expenses" name="Expenses" stroke="#ef4444" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
