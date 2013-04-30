#include <stddef.h>
#include <stdint.h>

// Find arg(max, next-to-max)
static inline void argmax2(const double *src, size_t *dest, size_t size)
{
	size_t imax1 = 0;
	size_t imax2 = 1;
	if (src[imax1] < src[imax2]) {
		imax1 = 1;
		imax2 = 0;
	}
	for (size_t i = 2; i < size; ++i) {
		if (src[i] > src[imax1]) {
			imax2 = imax1;
			imax1 = i;
		} else if (src[i] > src[imax2]) {
			imax2 = i;
		}
	}
	dest[0] = imax1;
	dest[1] = imax2;
}

static inline void min_update(double *a, double b) 
{
	if (*a > b)
		*a = b;
}

static inline void max_update(double *a, double b) 
{
	if (*a < b)
		*a = b;
}

static inline void minmax(const double *src, double *pmin, double *pmax, size_t N)
{
	*pmin = *pmax = src[0];
	for (size_t i = 0; i < N; ++i) {
		min_update(pmin, src[i]);
		max_update(pmax, src[i]);
	}
}

static inline double clip(double x) 
{
	return x > 255? 255 : x;
}

static inline void bfmov3(uint8_t *dest, const double *src)
{
	dest[0] = src[0];
	dest[1] = src[1];
	dest[2] = src[2];
}

static inline void bfmov3clip(uint8_t *dest, const double *src)
{
	dest[0] = clip(src[0]);
	dest[1] = clip(src[1]);
	dest[2] = clip(src[2]);
}

static inline void bfmov3k(uint8_t *dest, const double *src, double k)
{
	dest[0] = k * src[0];
	dest[1] = k * src[1];
	dest[2] = k * src[2];
}

static inline void fadd3k(double *dest, const double *src, double k)
{
	dest[0] += k * src[0];
	dest[1] += k * src[1];
	dest[2] += k * src[2];
}

/**********************
 *  Public interface  *
 **********************/

void visualize(
		// IN
		size_t N,
		size_t K,
		const double *Fprobs, // N x K
		const double *cmap, // K x 3
		// SCRATCH
		size_t *argmaxs, // N x 2
		double *diff_norms, // K
		double *ks, // K
		// OUT
		uint8_t *viz_argmax, // N x 3
		uint8_t *viz_intensity, // N x 3
		uint8_t *viz_linspace, // N x 3
		uint8_t *viz_linspace_clip, // N x 3
		uint8_t *viz_diff // N x 3
		) 
{
	double min_prob, max_prob;
	minmax(Fprobs, &min_prob, &max_prob, N*K);

	// Find argmax, argmax_2
	for (size_t i = 0; i < K; ++i)
		diff_norms[i] = 0;

	for (size_t i = 0; i < N; ++i) {
		argmax2(&Fprobs[K * i], &argmaxs[2 * i], K);
		max_update(
				&diff_norms[argmaxs[2 * i]], 
				Fprobs[K * i + argmaxs[2 * i]] 
                - Fprobs[K * i + argmaxs[2 * i + 1]]
				);
	}

	for (size_t i = 0; i < N; ++i) {
		size_t cmax = argmaxs[2 * i];
		size_t cmax2 = argmaxs[2 * i + 1];
		double lincol[3] = {0, 0, 0};
		double sum_ks = 0;
		double kdiff = (Fprobs[K * i + cmax] - Fprobs[K * i + cmax2]) 
            / diff_norms[cmax];

		for (size_t j = 0; j < K; ++j) {
			ks[j] = (Fprobs[K * i + j] - min_prob) 
                / (max_prob - min_prob + 1e-5);
			sum_ks += ks[j];

			fadd3k(lincol, &cmap[3 * j], ks[j]);
		}

		bfmov3(&viz_argmax[3 * i], &cmap[3 * cmax]);
		bfmov3k(&viz_intensity[3 * i], &cmap[3 * cmax], ks[cmax]);
		bfmov3k(&viz_diff[3 * i], &cmap[3 * cmax], kdiff);
		bfmov3k(&viz_linspace[3 * i], lincol, 1.0 / sum_ks);
		bfmov3clip(&viz_linspace_clip[3 * i], lincol);
	}
}

void test_gradient(
        size_t W,
        size_t H,
        uint8_t *img
        )
{
    for (size_t y = 0; y < H; ++y) {
        for (size_t x = 0; x < W; ++x) {
            img[3 * (W * y + x) + 0] = 255.0 * y / H;
            img[3 * (W * y + x) + 1] = 255.0 * x / W;
            img[3 * (W * y + x) + 2] = 255.0 * (x+y) / (W + H);
        }
    }
}

