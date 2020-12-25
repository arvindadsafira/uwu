package main
import "fmt"
import "math"
var hari, harga float64
func pem(kg float64) float64 {
	akhir := math.Round(kg)
	return akhir
}

func hit(kgc float64, sep float64, bed float64, harga *float64, hari *float64) {
	var hrg, hrg1, hrg2 float64
	var hr float64
	if int64(kgc)%2==0 {
		hr = kgc/2
	}else {
		hr = kgc/2 + 1
	}
	if sep!=0 && bed!=0 {
		*hari = hr + sep + bed
	}else if sep!=0 && bed==0 {
		*hari = hr + sep
	}else if sep==0 && bed!=0 {
		*hari = hr + bed
	} else {
		*hari = hr
	}
	hrg = kgc*6000
	hrg1 = sep*5000
	hrg2 = bed*10000
	*harga = hrg + hrg1 + hrg2
}

func main() {
	var ber, kg float64
	var sep, bed float64

	fmt.Print("Masukan berat cucian(kg): ")
	fmt.Scanln(&ber)
	fmt.Print("Masukan jumlah seprai: ")
	fmt.Scanln(&sep)
	fmt.Print("Masukan jumlah bed cover: ")
	fmt.Scanln(&bed)
	kg = pem(ber)
	hit(kg, sep, bed, &harga, &hari)
	fmt.Printf("Hasil pembulatan berat cucian(kg): %.f\n", kg)
	fmt.Printf("Lama pengerjaan(hari): %.f\n", hari)
	fmt.Printf("Biaya: Rp %.f\n", harga)
}