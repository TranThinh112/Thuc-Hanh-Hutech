using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using LT_Web_Buoi2.Models;
using LT_Web_Buoi2.Repositories;

namespace LT_Web_Buoi2.Controllers
{
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

        public IActionResult Index()
        {
            var products = _productRepository.GetAll();
            return View(products);
        }

        public IActionResult Add()
        {
            var categories = _categoryRepository.GetAllCategories();
            ViewBag.Categories = new SelectList(categories, "Id", "Name");

            return View();
        }
        
//them product moi
        [HttpPost]
        public async Task<IActionResult> Add(Product product, IFormFile? imageUrl, List<IFormFile>? imageUrls)
        {
            if (ModelState.IsValid)
            {
                if (imageUrl != null)
                {
                    product.ImageUrl = await SaveImage(imageUrl);
                }

                if (imageUrls != null && imageUrls.Count > 0)
                {
                    product.ImageUrls = new List<string>();

                    foreach (var file in imageUrls)
                    {
                        product.ImageUrls.Add(await SaveImage(file));
                    }
                }

                _productRepository.Add(product);
                return RedirectToAction("Index");
            }

            var categories = _categoryRepository.GetAllCategories();
            ViewBag.Categories = new SelectList(categories, "Id", "Name");

            return View(product);
        }

        public IActionResult Display(int id)
        {
            var product = _productRepository.GetById(id);

            if (product == null)
            {
                return NotFound();
            }

            return View(product);
        }

        public IActionResult Update(int id)
        {
            var product = _productRepository.GetById(id);

            if (product == null)
            {
                return NotFound();
            }

            var categories = _categoryRepository.GetAllCategories();
            ViewBag.Categories = new SelectList(categories, "Id", "Name", product.CategoryId);

            return View(product);
        }

//update product
        [HttpPost]
        public async Task<IActionResult> Update(Product product, IFormFile? imageUrl,  List<IFormFile>? imageUrls)
        {
            if (ModelState.IsValid)
            {
                var existingProduct = _productRepository.GetById(product.Id);

                if (existingProduct == null)
                {
                    return NotFound();
                }

                existingProduct.Name = product.Name;
                existingProduct.Price = product.Price;
                existingProduct.Description = product.Description;
                existingProduct.CategoryId = product.CategoryId;

                if (imageUrl != null)
                {
                    existingProduct.ImageUrl = await SaveImage(imageUrl);
                }

                // additional images
                if (imageUrls != null && imageUrls.Count > 0)
                {
                    existingProduct.ImageUrls ??= new List<string>();

                    foreach (var file in imageUrls)
                    {
                        existingProduct.ImageUrls.Add(await SaveImage(file));
                    }
                }

                _productRepository.Update(existingProduct);

                return RedirectToAction("Index");
            }

            var categories = _categoryRepository.GetAllCategories();

            //tao dropdown
            ViewBag.Categories = new SelectList(categories, "Id", "Name", product.CategoryId);

            return View(product);
        }

        public IActionResult Delete(int id)
        {
            var product = _productRepository.GetById(id);

            if (product == null)
            {
                return NotFound();
            }

            return View(product);
        }

//xoa product
        [HttpPost, ActionName("Delete")]
        public IActionResult DeleteConfirmed(int id)
        {
            _productRepository.Delete(id);
            return RedirectToAction("Index");
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
    }
}