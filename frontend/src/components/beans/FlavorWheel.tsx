"use client";

import { useState } from "react";
import { clsx } from "clsx";

interface FlavorWheelProps {
  flavors: { slug: string; name: string; category: string }[];
  selected: string[];
  onToggle: (slug: string) => void;
  maxSelections?: number;
}

const CATEGORY_COLORS: Record<string, string> = {
  フルーティ: "bg-red-100 text-red-800 border-red-200",
  フローラル: "bg-pink-100 text-pink-800 border-pink-200",
  スイート: "bg-amber-100 text-amber-800 border-amber-200",
  ナッティ: "bg-yellow-100 text-yellow-800 border-yellow-200",
  スパイシー: "bg-orange-100 text-orange-800 border-orange-200",
  ロースト: "bg-stone-200 text-stone-800 border-stone-300",
  セイボリー: "bg-green-100 text-green-800 border-green-200",
  発酵: "bg-purple-100 text-purple-800 border-purple-200",
};

export default function FlavorWheel({
  flavors,
  selected,
  onToggle,
  maxSelections = 5,
}: FlavorWheelProps) {
  // Group by category
  const grouped = flavors.reduce(
    (acc, f) => {
      const cat = f.category;
      if (!acc[cat]) acc[cat] = [];
      acc[cat].push(f);
      return acc;
    },
    {} as Record<string, typeof flavors>
  );

  return (
    <div className="space-y-3">
      {Object.entries(grouped).map(([category, items]) => (
        <div key={category}>
          <h4 className="text-xs font-medium text-stone-500 mb-1.5 uppercase tracking-wider">
            {category}
          </h4>
          <div className="flex flex-wrap gap-1.5">
            {items.map((flavor) => {
              const isSelected = selected.includes(flavor.slug);
              const isDisabled =
                !isSelected && selected.length >= maxSelections;
              return (
                <button
                  key={flavor.slug}
                  type="button"
                  onClick={() => !isDisabled && onToggle(flavor.slug)}
                  disabled={isDisabled}
                  className={clsx(
                    "px-2.5 py-1 rounded-full text-xs font-medium border transition-all",
                    isSelected
                      ? "bg-amber-900 text-white border-amber-900 shadow-sm"
                      : CATEGORY_COLORS[category] || "bg-stone-100 text-stone-700 border-stone-200",
                    isDisabled && "opacity-40 cursor-not-allowed",
                    !isDisabled && !isSelected && "hover:shadow-sm"
                  )}
                >
                  {flavor.name}
                </button>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}
