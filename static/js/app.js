
const SOVA_PRODUCTS = {
  afnan: {
    name: "Afnan 9 PM",
    price: 65000,
    image: "static/images/afnan.jpg"
  },
  asad: {
    name: "Lattafa Asad",
    price: 45000,
    image: "static/images/asad.jpg"
  },
  freeze: {
    name: "Freeze Riiffs",
    price: 50000,
    image: "static/images/FREEZE RIIFFS.jpg"
  },
  flames: {
    name: "Freeze In Flames Riiffs",
    price: 50000,
    image: "static/images/FREEZE IN FLAMES RIIFFS.jpg"
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
  if (!SOVA_PRODUCTS[id]) return;

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
        <img src="${product.image}" alt="${product.name}"
             style="width:85px;height:95px;object-fit:contain">
        <div>
          <h3>${product.name}</h3>
          <p>${sovaFormatPrice(product.price)}</p>
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
  if (totalElement) totalElement.textContent = sovaFormatPrice(total);

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
    lines.push(`${product.name} × ${quantity} = ${sovaFormatPrice(subtotal)}`);
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

  const url = "https://wa.me/9647806364447?text=" + encodeURIComponent(message);
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
