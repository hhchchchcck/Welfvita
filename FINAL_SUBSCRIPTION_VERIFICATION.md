# کنترل نهایی صفحهٔ Subscription RVG

این نسخه با بخش `SubPage` و `SubUsageSummary` در سورس مرجع 3x-ui مقایسه و برای محیط RVG بدون وابستگی React یا Ant Design پیاده‌سازی شده است. فرانت RVG اکنون از همان قرارداد داده‌ای `window.__SUB_PAGE_DATA__` استفاده می‌کند و backend تک‌کاربرهٔ RVG همان View Model شامل `sId`، وضعیت، ترافیک byte-level، انقضا، URLها، title، لینک‌ها و ایمیل/برچسب‌ها را server-side bootstrap می‌کند. ساختار عملیاتی شامل عنوان و شناسهٔ Subscription، کنترل دایره‌ای تم و زبان در هدر، جدول وضعیت، کارت مصرف و انقضا، بخش Subscription info، ردیف Copy All Configs، ردیف هر کانفیگ، QR، و منوهای Android/iOS است.

| معیار پذیرش | نتیجه |
| --- | --- |
| بازکردن `/sub/{uuid}` در مرورگر | صفحهٔ HTML Subscription info از `window.__SUB_PAGE_DATA__` با ظاهر و ساختار نزدیک به 3x-ui نمایش داده می‌شود |
| بازکردن `/sub/{uuid}` با User-Agent کلاینت VPN | feed استاندارد Base64 و هدرهای subscription بازگردانده می‌شود |
| بازکردن `/sub/{uuid}?view=raw` | feed خام Base64 اجباری بازگردانده می‌شود |
| بازکردن `/sub-group/{uuid}` در مرورگر | همان رابط Subscription info برای گروه نمایش داده می‌شود |
| سابسکریپشن رمزدار گروهی | فرم رمز در مرورگر و feed محافظت‌شده در کلاینت حفظ می‌شود |
| اجزای رابط مرجع 3x-ui | جدول، سهمیه/مصرف، countdown انقضا، Copy/QR، Copy All و Android/iOS پوشش داده شده‌اند |

آزمون یکپارچهٔ `test_subscription_integration.py` در بسته اجرا شده است و مسیرهای مرورگر، bootstrap contract، API تک‌کاربره، feed کلاینت‌های V2RayNG، v2rayN، V2Box، sing-box، Clash/Mihomo، Hiddify، Shadowrocket، V2RayTun، NPV Tunnel، Happ، Incy و Streisand، حالت raw، API گروه و سابسکریپشن رمزدار را بررسی می‌کند.
