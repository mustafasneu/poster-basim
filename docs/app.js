/* Hero düğmesini ziyaretçinin işletim sistemine göre ayarlar.
   Tanınmazsa düğme indirme bölümüne götürmeye devam eder — kimse açıkta kalmaz. */

document.documentElement.classList.add("js");

(function () {
    const btn = document.getElementById("ana-indirme");
    if (!btn) return;

    const label = document.getElementById("ana-indirme-yazi");
    const ua = navigator.userAgent;
    const platform = navigator.userAgentData?.platform || navigator.platform || "";
    const hay = (ua + " " + platform).toLowerCase();

    let key = null;
    if (hay.includes("win")) key = "win";
    else if (hay.includes("mac") && !hay.includes("iphone") && !hay.includes("ipad")) key = "mac";
    else if (hay.includes("linux") && !hay.includes("android")) key = "linux";

    if (!key) return;

    const href = btn.dataset[key];
    if (!href) return;

    btn.href = href;

    const wording =
        document.documentElement.lang === "en"
            ? { win: "Download for Windows", mac: "Download for macOS", linux: "Download for Linux" }
            : { win: "Windows için indir", mac: "macOS için indir", linux: "Linux için indir" };

    if (label) label.textContent = wording[key];
})();
