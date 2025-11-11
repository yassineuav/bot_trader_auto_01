"use client";

import { create } from "zustand";

type SettingsState = {
  theme: "dark" | "light";
  toggleTheme: () => void;
};

export const useSettings = create<SettingsState>((set) => ({
  theme: "dark",
  toggleTheme: () => set((state) => ({ theme: state.theme === "dark" ? "light" : "dark" })),
}));
