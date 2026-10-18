const products = {

    iphone: {
        title: "Iphone 17 Mau Cam",
        price: "$1000",
        image: "/image/ip17.png",

        description:
        "Đẹp nhưng hao pin.",

        ram: "12GB",
        memory: "512GB",
        camera: "200MP",
        pin: "6000mAh"
    },

    boeing: {
        title: "May Bay Boeing",
        price: "$2000",
        image: "/image/boeing.png",

        description:
        "Máy Bay Đua.",

        ram: "Khong co",
        memory: "Radar Quan Su",
        camera: "Camera Nhiet",
        pin: "Dong co Phan Luc"
    },

    samsung: {
        title: "Samsung S24 Ultra",
        price: "$2000",
        image: "/image/SSumS24.png",

        description:
        "Samsung flagship màn hình đẹp.",

        ram: "16GB",
        memory: "1TB",
        camera: "250MP",
        pin: "7000mAh"
    },
    dothai: {
        title: "Người Do Thái",
        price: "$20",
        image: "/image/NguoiDoThai.png",

        description:
        "Thông Minh Hơn Người.",

        ram: "Vo Cuc",
        memory: "Vo Cuc",
        camera: "500mp",
        pin: "20 năm"
    },
    tuong: {
        title: "Tượng Nữ Thần Tự Do",
        price: "$1000",
        image: "/image/tuongnuathantudo.png",

        description:
        "Trang Trí Thì Ngon Luôn.",

        ram: "Không có",
        memory: "Không có",
        camera: "Không có",
        pin: "Vĩnh Viễn"
    },
    daden: {
        title: "Người Da Đen",
        price: "$1000",
        image: "/image/nguoidaden.png",

        description:
        "Giúp Việc Thì ngon Luôn.",

        ram: "Không có",
        memory: "Không có",
        camera: "Không có",
        pin: "Vĩnh Viễn"
    },
    tim: {
        title: "Tim Người Da Đen",
        price: "$1000",
        image: "/image/tim.png",

        description:
        "Hỗ Trợ Bơm Máu.",

        ram: "Không có",
        memory: "Không có",
        camera: "Không có",
        pin: "Vĩnh Viễn"
    },
    hutech: {
        title: "Đại Học Hutech",
        price: "$1000",
        image: "/image/hutech.png",

        description:
        "Đại Học Quận 9.",

        ram: "Không có",
        memory: "Không có",
        camera: "Không có",
        pin: "Vĩnh Viễn"
    },
    

    tenlua: {
        title: "Tên Lửa Đạn Đạo",
        price: "$50000",
        image: "/image/tenluadandao.png",

        description:
        "Tên Lửa Đạn Đạo Xuyên Lục Địa 10000km.",

        ram: "He thong AI",
        memory: "Dinh vi Ve Tinh",
        camera: "Camera Hong Ngoai",
        pin: "Dong co Hat Nhan"
    }

};

  const params =
        new URLSearchParams(window.location.search);

    const id = params.get("id");


    const product = products[id];


    document.getElementById("title").innerText =
        product.title;

    document.getElementById("price").innerText =
        product.price;

    document.getElementById("image").src =
        product.image;

    document.getElementById("description").innerText =
        product.description;

        document.getElementById("ram").innerText =
    product.ram;

document.getElementById("memory").innerText =
    product.memory;

document.getElementById("camera").innerText =
    product.camera;

document.getElementById("pin").innerText =
    product.pin;
