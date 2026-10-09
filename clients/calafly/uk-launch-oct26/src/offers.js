// Single source for prices, promo codes, small print and local wording across every CalaFly creative and video.
// A country set to null renders without a price; fill it in and re-render once the plan price is confirmed.
window.OFFERS = (() => {
  const TERMS = "calafly.net/legal/terms";
  const O = {
    usa: { data: "3GB", price: 7, days: 30, code: "USA10", pct: 10, couch: true },
    turkey: null,   // price to come from calafly.net
    dubai: null,    // price to come from calafly.net
  };
  const gbp = n => "£" + (Number.isInteger(n) ? n : n.toFixed(2));
  const api = {
    TERMS,
    // Refund promise, worded the same on every creative
    REFUND: "100% refund if unused",
    REFUND_LONG: "100% refund, guaranteed, if your eSIM is unused.",
    get: k => O[k] || null,
    price: k => O[k] ? gbp(O[k].price) : "",
    promoPrice: k => O[k] && O[k].code ? gbp(Math.round(O[k].price * (100 - O[k].pct)) / 100) : "",
    plan: k => O[k] ? `${O[k].data} · ${O[k].days} days` : "",
    // US English for the USA creatives ("couch"); UK wording elsewhere
    sofa: k => O[k] && O[k].couch ? "couch" : "sofa",
    // One short small-print line: claims qualification, material info, promo terms, then the T&Cs URL.
    small: (k, { refund = false } = {}) => {
      const o = O[k], parts = [];
      if (refund) parts.push("100% refund if your eSIM is unused.");
      parts.push("Data-only eSIM. Unlocked, eSIM-compatible phone needed.");
      if (o && o.code) parts.push(`${o.code}: ${o.pct}% off first order, new customers only.`);
      parts.push(`T&amp;Cs apply: ${TERMS}`);
      return parts.join(" ");
    },
  };
  return api;
})();
