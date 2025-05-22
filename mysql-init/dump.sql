SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET collation_connection = utf8mb4_unicode_ci;

-- MySQL dump with only INSERT statements
SET FOREIGN_KEY_CHECKS=0;


-- Insert categories
INSERT INTO `products_category` (`id`, `name`, `description`, `created_at`, `updated_at`) VALUES 
(1,'Süt Ürünleri','Süt ve süt ürünleri kategorisi','2025-04-26 23:46:30.008465','2025-04-26 23:46:30.008465'),
(2,'Sebzeler','Taze sebzeler kategorisi','2025-04-26 23:46:30.008465','2025-04-26 23:46:30.008465'),
(3,'Macunlar','Doğal macunlar kategorisi','2025-04-26 23:46:30.008465','2025-04-26 23:46:30.008465'),
(4,'Atıştırmalıklar','Sağlıklı atıştırmalıklar kategorisi','2025-04-26 23:46:30.008465','2025-04-26 23:46:30.008465'),
(5,'Meyveler','Taze meyveler kategorisi','2025-04-26 23:46:30.008465','2025-04-26 23:46:30.008465');

-- Insert products
INSERT INTO `products_product` (`id`, `name`, `model`, `serial_number`, `description`, `price`, `stock_quantity`, `category_id`, `warranty_status`, `distributor_info`, `image_url`, `rating_count`, `avg_rating`, `created_at`, `updated_at`) VALUES 
(1,'10\'lu Organik Yumurta','ORG-MODEL-1','SN001ABC','Serbest dolaşan tavuklardan elde edilen taze organik yumurta.',39.90,12,1,0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/50524/uploads/urunresimleri/buyuk/10lu-gezen-tavuk-yumurtasi-fe5899.jpg',0,0,'2025-04-26 23:46:30.008465','2025-04-26 23:46:30.008465'),
(2,'Organik Süt (1L)','ORG-MODEL-2','SN002ABC','Taze ve doğal organik süt.',24.50,0,1,0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/56277/uploads/urunresimleri/buyuk/akmese-organik-sut-3lt-sadece-bursa-ve-dc0e09.png',5,1,'2025-04-26 23:46:30.008465','2025-04-26 23:46:30.008465'),
(3,'Organik Peynir (500g)','ORG-MODEL-3','SN003ABC','El yapımı, lezzetli ve sağlıklı organik peynir.',45.90,14,1,0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/56277/uploads/urunresimleri/buyuk/100-salamura-keci-peyniri-400-gr-8a5-c9.png',0,0,'2025-04-26 23:46:30.008465','2025-04-26 23:46:30.008465'),
(4,'Domates (1 kg)','ORG-MODEL-4','SN004ABC','Taze ve organik domatesler, sağlıklı yemekler için ideal.',19.90,22,2,0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/56277/uploads/urunresimleri/buyuk/organik-sofralik-domates-1-kg-sadece-b-ef144f.jpeg',0,0,'2025-04-26 23:46:30.008465','2025-04-26 23:46:30.008465'),
(5,'Kozalak Macunu 240 g','ORG-MODEL-5','SN005ABC','Doğal içeriğiyle kozalağın faydalarını sunan macun.',150.90,6,3,0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=360,quality=85/56277/uploads/urunresimleri/buyuk/og-kozalak-macunu-240-gr-cf2-9f.jpg',0,0,'2025-04-26 23:46:30.008465','2025-04-26 23:46:30.008465'),
(6,'Jovia Organik %70 Bitter Çikolata-Yaban Mersini&Badem&Açai','ORG-MODEL-6','SN006ABC','Zengin kakao aroması ve organik içeriğiyle bitter çikolata keyfi.',220.90,5,4,0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=360,quality=85/56277/uploads/urunresimleri/buyuk/jovia-organik-70-bitter-cikolata-yaban-d3ef-4.jpg',0,0,'2025-04-26 23:46:30.008465','2025-04-26 23:46:30.008465'),
(7,'Taze Kuşkonmaz(1 kg)','ORG-MODEL-7','SN007ABC','Vitamin deposu taze kuşkonmaz, sağlıklı beslenme için.',27.90,9,2,0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/56277/uploads/urunresimleri/buyuk/taze-kuskonmaz--b-4ec9.jpg',0,0,'2025-04-26 23:46:30.008465','2025-04-26 23:46:30.008465'),
(8,'Taze Böğürtlen','ORG-MODEL-8','SN008ABC','Tatlı ve taze böğürtlen, doğal atıştırmalık olarak ideal.',240.90,4,5,0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/56277/uploads/urunresimleri/buyuk/taze-bogurtlen-213f64.jpg',0,0,'2025-04-26 23:46:30.008465','2025-04-26 23:46:30.008465'),
(9,'Kara Mürver Püresi','ORG-MODEL-9','SN009ABC','Doğal ve besleyici kara mürver püresi.',225.00,3,3,0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/56277/uploads/urunresimleri/buyuk/kara-murver-puresi-230g--46d1-.jpg',0,0,'2025-04-26 23:46:30.008465','2025-04-26 23:46:30.008465'),
(10,'Taze Zerdeçal(80 gr)','ORG-MODEL-10','SN010ABC','Antioksidan özellikleriyle taze zerdeçal.',75.90,7,2,0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/56277/uploads/urunresimleri/buyuk/taze-zerdecal-100gr-935-38.jpeg',0,0,'2025-04-26 23:46:30.008465','2025-04-26 23:46:30.008465'),
(11,'Taze Zencefil (1 kg)','ORG-MODEL-11','SN011ABC','Baharat olarak veya sağlık amaçlı kullanabileceğiniz taze zencefil.',16.90,10,2,0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/56277/uploads/urunresimleri/buyuk/taze-zencefil-250gpaket-7-e72f.jpg',0,0,'2025-04-26 23:46:30.008465','2025-04-26 23:46:30.008465'),
(12,'Tatlı Patates (1 kg)','ORG-MODEL-12','SN012ABC','Lezzetli ve besleyici tatlı patates.',54.90,15,2,0,'Default Distributor','https://static.ticimax.cloud/cdn-cgi/image/width=-,quality=85/56277/uploads/urunresimleri/buyuk/tatli-patates-2-kg-da-734.jpg',0,0,'2025-04-26 23:46:30.008465','2025-04-26 23:46:30.008465');

SET FOREIGN_KEY_CHECKS=1;