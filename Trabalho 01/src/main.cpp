#include <vector>
#include <iostream>
#include <FreeImagePlus.h>
#include <xtensor/xarray.hpp>
#include <xtensor/xadapt.hpp>
#include <xtensor/xio.hpp>


int main() {
    fipImage fip;
    fip.load("Imagens/city.png");

    std::vector<unsigned char> imagem = {fip.accessPixels(), fip.accessPixels() + fip.getImageSize()};
    std::vector<std::size_t> shape = {fip.getWidth(), fip.getHeight()};
    auto arr = xt::xadapt(imagem, shape);

    std::cout << arr;
    return 0;
}
