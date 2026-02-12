"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import Button from "@/components/ui/Button";
import Select from "@/components/ui/Select";
import Textarea from "@/components/ui/Textarea";
import FlavorWheel from "@/components/beans/FlavorWheel";
import type { ReviewCreate } from "@/types/review";

const reviewSchema = z.object({
  rating: z.number().min(1).max(5),
  brew_method: z.string().optional(),
  comment: z.string().max(1000).optional(),
});

interface ReviewFormProps {
  flavors: { slug: string; name: string; category: string }[];
  onSubmit: (data: ReviewCreate) => void;
  isSubmitting?: boolean;
}

export default function ReviewForm({
  flavors,
  onSubmit,
  isSubmitting,
}: ReviewFormProps) {
  const t = useTranslations();
  const [selectedFlavors, setSelectedFlavors] = useState<string[]>([]);
  const [rating, setRating] = useState(0);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(reviewSchema),
  });

  const toggleFlavor = (slug: string) => {
    setSelectedFlavors((prev) =>
      prev.includes(slug) ? prev.filter((s) => s !== slug) : [...prev, slug]
    );
  };

  const onFormSubmit = (data: any) => {
    onSubmit({
      rating,
      flavor_notes: selectedFlavors,
      brew_method: data.brew_method || undefined,
      comment: data.comment || undefined,
    });
  };

  const brewMethodOptions = [
    { value: "pour_over", label: t("brewMethods.pour_over") },
    { value: "espresso", label: t("brewMethods.espresso") },
    { value: "french_press", label: t("brewMethods.french_press") },
    { value: "aeropress", label: t("brewMethods.aeropress") },
    { value: "siphon", label: t("brewMethods.siphon") },
    { value: "cold_brew", label: t("brewMethods.cold_brew") },
    { value: "other", label: t("brewMethods.other") },
  ];

  return (
    <form onSubmit={handleSubmit(onFormSubmit)} className="space-y-6">
      {/* Rating */}
      <div>
        <label className="block text-sm font-medium text-stone-700 mb-2">
          {t("reviews.rating")}
        </label>
        <div className="flex gap-1">
          {[1, 2, 3, 4, 5].map((star) => (
            <button
              key={star}
              type="button"
              onClick={() => setRating(star)}
              className="text-3xl transition-colors"
            >
              <span className={star <= rating ? "text-amber-500" : "text-stone-300"}>
                ★
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Flavor Notes */}
      <div>
        <label className="block text-sm font-medium text-stone-700 mb-2">
          {t("reviews.flavorNotes")}
          <span className="text-xs text-stone-400 ml-1">
            ({selectedFlavors.length}/5)
          </span>
        </label>
        <FlavorWheel
          flavors={flavors}
          selected={selectedFlavors}
          onToggle={toggleFlavor}
          maxSelections={5}
        />
      </div>

      {/* Brew Method */}
      <Select
        label={t("reviews.brewMethod")}
        options={brewMethodOptions}
        placeholder="---"
        {...register("brew_method")}
      />

      {/* Comment */}
      <Textarea
        label={t("reviews.comment")}
        placeholder={t("reviews.commentPlaceholder")}
        maxLength={1000}
        {...register("comment")}
        error={errors.comment?.message as string}
      />

      {/* Submit */}
      <Button
        type="submit"
        size="lg"
        className="w-full"
        disabled={rating === 0 || isSubmitting}
      >
        {isSubmitting ? t("common.loading") : t("reviews.submit")}
      </Button>
    </form>
  );
}
