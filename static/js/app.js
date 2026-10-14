const SOVA_PRODUCTS = {
  "afnan": {
    name: "Afnan 9 PM",
    price: 65000,
    image: "static/images/AFNAN.jpg"
  },
  "asad": {
    name: "Lattafa Asad",
    price: 45000,
    image: "static/images/ASAD.jpg"
  },
  "freeze": {
    name: "Freeze Riiffs",
    price: 50000,
    image: "static/images/FREEZE RIIFFS.jpg"
  },
  "flames": {
    name: "Freeze In Flames Riiffs",
    price: 50000,
    image: "static/images/FREEZE IN FLAMES RIIFFS.jpg"
  },
  "night-out": {
    name: "Afnan 9 PM Night Out",
    price: 65000,
    image: "static/images/night-out.jpg"
  },
  "supremacy-ce": {
    name: "Supremacy Collector's Edition",
    price: 70000,
    image: "static/images/supremacy-ce.jpg"
  },
  "hawas-ice": {
    name: "Hawas Ice",
    price: 45000,
    image: "static/images/hawas-ice.jpg"
  },
  "hawas-black": {
    name: "Hawas Black",
    price: 45000,
    image: "static/images/hawas-black.jpg"
  },
  "hawas-kobra": {
    name: "Hawas Kobra",
    price: 45000,
    image: "static/images/hawas-kobra.jpg"
  }
};

const SOVA_CART_KEY = "sova_cart";

function sovaGetCart() {
  try {
    const cart = JSON.parse(localStorage.getItem(SOVA_CART_KEY) || "{}");
    return cart && typeof cart === "object" && !Array.isArray(cart)
      ? cart
      : {};
  } catch {
    return {};
  }
}

function sovaSaveCart(cart) {
  localStorage.setItem(SOVA_CART_KEY, JSON.stringify(cart));
  sovaUpdateCartCount();
}

function sovaUpdateCartCount() {
  const cart = sovaGetCart();

  const count = Object.values(cart).reduce(
    (sum, quantity) => sum + Math.max(0, Number(quantity) || 0),
    0
  );

  document.querySelectorAll("[data-cart-count]").forEach(element => {
    element.textContent = count;
  });
}

function sovaAddToCart(id) {
  if (!SOVA_PRODUCTS[id]) {
    alert("هذا العطر غير موجود حالياً 💙");
    return;
  }

  const cart = sovaGetCart();
  cart[id] = (Number(cart[id]) || 0) + 1;

  sovaSaveCart(cart);
  alert("انضاف العطر للسلة بنجاح 💙");
}

function sovaChangeQuantity(id, change) {
  if (!SOVA_PRODUCTS[id]) return;

  const cart = sovaGetCart();
  const quantity = (Number(cart[id]) || 0) + change;

  if (quantity <= 0) {
    delete cart[id];
  } else {
    cart[id] = quantity;
  }

  sovaSaveCart(cart);
  sovaRenderCart();
}

function sovaRemoveFromCart(id) {
  const cart = sovaGetCart();
  delete cart[id];

  sovaSaveCart(cart);
  sovaRenderCart();
}

function sovaFormatPrice(price) {
  return Number(price).toLocaleString("en-US") + " د.ع";
}

function sovaRenderCart() {
  const container = document.getElementById("cart-items");
  if (!container) return;

  const cart = sovaGetCart();
  let total = 0;
  let html = "";

  Object.entries(cart).forEach(([id, quantity]) => {
    const product = SOVA_PRODUCTS[id];
    quantity = Math.max(0, Number(quantity) || 0);

    if (!product || quantity < 1) return;

    const subtotal = product.price * quantity;
    total += subtotal;

    html += `
      <article class="cart-item">
        <img
          src="${product.image}"
          alt="${product.name}"
          loading="lazy"
          style="width:100px;height:110px;object-fit:contain;flex-shrink:0;background:#081727;border-radius:6px"
          onerror="this.style.display='none';this.nextElementSibling.style.display='block'"
        >
        <div style="display:none;color:#8cddff;font-size:12px;min-width:85px">
          صورة العطر غير متوفرة
        </div>

        <div style="flex:1;min-width:0">
          <h3>${product.name}</h3>
          <p>سعر القطعة: ${sovaFormatPrice(product.price)}</p>

          <button type="button" data-cart-action="minus" data-id="${id}">−</button>
          <span>${quantity}</span>
          <button type="button" data-cart-action="plus" data-id="${id}">+</button>
          <button type="button" data-cart-action="remove" data-id="${id}">
            حذف
          </button>

          <p>المجموع: ${sovaFormatPrice(subtotal)}</p>
        </div>
      </article>
    `;
  });

  container.innerHTML = html || "<p>سلتك فارغة حالياً 💙</p>";

  const totalElement = document.getElementById("cart-total");
  if (totalElement) {
    totalElement.textContent = sovaFormatPrice(total);
  }

  sovaUpdateCartCount();
}

function sovaCheckout() {
  const cart = sovaGetCart();
  const lines = [];
  let total = 0;

  Object.entries(cart).forEach(([id, quantity]) => {
    const product = SOVA_PRODUCTS[id];
    quantity = Math.max(0, Number(quantity) || 0);

    if (!product || quantity < 1) return;

    const subtotal = product.price * quantity;
    total += subtotal;

    lines.push(
      `${product.name} × ${quantity} = ${sovaFormatPrice(subtotal)}`
    );
  });

  if (!lines.length) {
    alert("السلة فارغة، أضف عطراً أولاً 💙");
    return;
  }

  const message = [
    "السلام عليكم، أريد أطلب من SOVA:",
    "",
    ...lines,
    "",
    `المجموع الكلي: ${sovaFormatPrice(total)}`,
    "",
    "يرجى تأكيد الطلب والتوصيل."
  ].join("\n");

  const url =
    "https://wa.me/9647806364447?text=" +
    encodeURIComponent(message);

  window.open(url, "_blank", "noopener,noreferrer");
}

document.addEventListener("click", event => {
  const button = event.target.closest("[data-cart-action]");
  if (!button) return;

  const id = button.dataset.id;
  const action = button.dataset.cartAction;

  if (action === "plus") sovaChangeQuantity(id, 1);
  if (action === "minus") sovaChangeQuantity(id, -1);
  if (action === "remove") sovaRemoveFromCart(id);
});

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-add-to-cart]").forEach(button => {
    button.addEventListener("click", () => {
      sovaAddToCart(button.dataset.addToCart);
    });
  });

  document.querySelectorAll("[data-checkout]").forEach(button => {
    button.addEventListener("click", sovaCheckout);
  });

  sovaUpdateCartCount();
  sovaRenderCart();
});
