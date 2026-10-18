using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Web_buoi_6.Models_Shop;


using Microsoft.AspNetCore.Authorization;

[Area("Admin")]
[Authorize(Roles = "Admin")]
public class ProductController : Controller
{
     private readonly IProductRepository _productRepository;
        private readonly ICategoryRepository _categoryRepository;

         private readonly IWebHostEnvironment _webHostEnvironment;

        public ProductController(
           IProductRepository productRepository,
           ICategoryRepository categoryRepository,
             IWebHostEnvironment webHostEnvironment)
        {
            _productRepository = productRepository;
            _categoryRepository = categoryRepository;
             _webHostEnvironment = webHostEnvironment;
        }


        public async Task<IActionResult> Index()
        {
            var products = await _productRepository.GetAllAsync();
            return View(products);
        }

        public async Task<IActionResult> Create()
        {
            var categories = await _categoryRepository.GetAllAsync();
            ViewBag.Categories = new SelectList(categories, "Id", "Name");

            return View();
        }


        //luu hinh anh vao thu muc wwwroot/images va tra ve duong dan de luu vao database
        private async Task<string> SaveImage(IFormFile image)
        {

            //duong dan thu muc wwwroot/images
            var imagesFolder = Path.Combine(_webHostEnvironment.WebRootPath, "images");

            if (!Directory.Exists(imagesFolder))
            {
                Directory.CreateDirectory(imagesFolder);
            }

            var fileName = Guid.NewGuid().ToString() + Path.GetExtension(image.FileName);
            var savePath = Path.Combine(imagesFolder, fileName);

            using (var fileStream = new FileStream(savePath, FileMode.Create))
            {
                await image.CopyToAsync(fileStream);
            }

            return "/images/" + fileName;
        }

        //them product moi
        [HttpPost]
        public async Task<IActionResult> Create(Product product, IFormFile? imageUrl)
        {
            if (ModelState.IsValid)
            {
                if (imageUrl != null)
                {
                    product.ImageUrl = await SaveImage(imageUrl);
                }

                await _productRepository.AddAsync(product);

                return RedirectToAction("Index");
            }

            var categories = await _categoryRepository.GetAllAsync();
            ViewBag.Categories = new SelectList(categories, "Id", "Name");

            return View(product);
        }

        public  async Task<IActionResult> Display(int id)
        {
            var product = await _productRepository.GetByIdAsync(id);

            if (product == null)
            {
                return NotFound();
            }

            return View(product);
        }

        public async Task<IActionResult> Update(int id)
        {
            var product = await _productRepository.GetByIdAsync(id);

            if (product == null)
            {
                return NotFound();
            }

            var categories = await _categoryRepository.GetAllAsync();
            ViewBag.Categories = new SelectList(categories, "Id", "Name", product.CategoryId);

            return View(product);
        }

        //update product
        [HttpPost]
        public async Task<IActionResult> Update(Product existingProduct, IFormFile? imageUrl)
        {
            if (ModelState.IsValid)
            {
                if (imageUrl != null)
                {
                    existingProduct.ImageUrl = await SaveImage(imageUrl);
                }

                await _productRepository.UpdateAsync(existingProduct);

                return RedirectToAction("Index");
            }

            return View(existingProduct);
        }

        public async Task<IActionResult> Delete(int id)
        {
            var product = await _productRepository.GetByIdAsync(id);

            if (product == null)
            {
                return NotFound();
            }

            return View(product);
        }

        //xoa product
        [HttpPost, ActionName("Delete")]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            await _productRepository.DeleteAsync(id);
            return RedirectToAction(nameof(Index));
        }
    }