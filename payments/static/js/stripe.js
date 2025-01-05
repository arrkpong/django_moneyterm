// payments/static/js/stripe.js

// ตรวจสอบว่าคอนโซลทำงานโดยการบันทึกข้อความนี้ลงในคอนโซล
console.log("Sanity check!");

document.addEventListener('DOMContentLoaded', function () {
    // ตรวจสอบว่ามีปุ่ม submit อยู่หรือไม่
    if (document.querySelector("#submitBtn")) {
        // ทำ fetch ไปยัง URL /config/ และดำเนินการต่อไปเมื่อมีปุ่ม submit อยู่
        fetch("/config/")
        .then((result) => {
            // บันทึกข้อความเพื่อแสดงว่าเริ่มดึงข้อมูลการตั้งค่า
            console.log("Fetching config");
            // แปลงผลลัพธ์ที่ได้รับเป็น JSON
            return result.json();
        })
        .then((data) => {
            // บันทึกข้อมูลการตั้งค่าที่ได้รับลงในคอนโซล
            console.log("Config data received", data);
            // กำหนดค่าเริ่มต้นให้ stripe ด้วย public key ที่ได้รับ
            const stripe = Stripe(data.publicKey);

            // เพิ่มตัวจัดการเหตุการณ์สำหรับปุ่ม submit
            document.querySelector("#submitBtn").addEventListener("click", () => {
                // บันทึกข้อความเมื่อปุ่ม submit ถูกคลิก
                console.log("Submit button clicked");
                // เริ่มต้นการร้องขอเพื่อสร้าง checkout session
                fetch("/create-checkout-session/")
                .then((result) => {
                    // บันทึกข้อความเพื่อแสดงว่าเริ่มสร้าง checkout session  
                    console.log("Creating checkout session");
                    // แปลงผลลัพธ์ที่ได้รับเป็น JSON
                    return result.json();
                })
                .then((data) => {
                    // บันทึกข้อมูลของ checkout session ที่ได้รับลงในคอนโซล
                    console.log("Checkout session data received", data);
                    // ตรวจสอบว่ามี session ID ที่ได้รับหรือไม่
                    if (data.sessionId) {
                        // นำผู้ใช้ไปยังหน้า checkout โดยใช้ session ID ที่ได้รับ
                        stripe.redirectToCheckout({ sessionId: data.sessionId });
                    } else {
                        // กรณีที่ไม่มี session ID ที่ได้รับ
                        console.error("No session ID received");
                    }
                })
                .catch((error) => {
                    // กรณีที่มีข้อผิดพลาดในการสร้าง checkout session
                    console.error("Error creating checkout session:", error);
                });
            });
        })
        .catch((error) => {
            // กรณีที่มีข้อผิดพลาดในการเรียก config
            console.error("Error fetching config:", error);
        });
    }
});

