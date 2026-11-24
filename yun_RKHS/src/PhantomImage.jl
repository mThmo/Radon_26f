module MyPhantomTestImg
# Phantom test images for tomography experiments.
# Loaded in main_tomo_recons.jl by:
#     include("src/PhantomImage.jl")
#     using .MyPhantomTestImg
# and called as MyPhantomTestImg.shepp_logan(M) / MyPhantomTestImg.random_circles(M; n_circles=20).

export shepp_logan      # Shepp-Logan phantom
export random_circles   # Random ellipses inside the unit disk

# Shepp-Logan phantom (formerly in Images.jl).
# L. A. Shepp and B. F. Logan (1974), "The Fourier reconstruction of a head section",
# IEEE Trans. Nuclear Science NS-21.
"""
    shepp_logan(M, N; highContrast=true)
    shepp_logan(N; highContrast=true)

Return the M×N (or N×N) Shepp-Logan phantom on the grid `-1 + k/div(N,2)`, k = 0,…,N-1.
`highContrast=true` gives the MRI-style contrast used in the Yun–Panaretos experiments;
`false` gives the original CT gray levels.
"""
function shepp_logan(M::Int64, N::Int64; highContrast=true)
    P = zeros(M, N)

    x = ((0:(N-1)) / div(N, 2) .- 1)'   # 1×N row (columns ↔ x)
    y = ((0:(M-1)) / div(M, 2) .- 1)    # M×1 column (rows ↔ y)

    centerX   = [0, 0, 0.22, -0.22, 0, 0, 0, -0.08, 0, 0.06]
    centerY   = [0, -0.0184, 0, 0, 0.35, 0.1, -0.1, -0.605, -0.605, -0.605]
    majorAxis = [0.69, 0.6624, 0.11, 0.16, 0.21, 0.046, 0.046, 0.046, 0.023, 0.023]
    minorAxis = [0.92, 0.874, 0.31, 0.41, 0.25, 0.046, 0.046, 0.023, 0.023, 0.046]
    theta     = [0, 0, -18.0, 18.0, 0, 0, 0, 0, 0, 0]   # degrees

    # original (CT) gray levels
    grayLevel = [2, -0.98, -0.02, -0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
    if highContrast
        # high-contrast (MRI) gray levels
        grayLevel = [1, -0.8, -0.2, -0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    end

    for l in eachindex(theta)
        c = cos(theta[l] / 360 * 2 * pi)
        s = sin(theta[l] / 360 * 2 * pi)
        P += grayLevel[l] * (
            ((c * (x .- centerX[l]) .+ s * (y .- centerY[l])) / majorAxis[l]) .^ 2 .+
            ((s * (x .- centerX[l]) .- c * (y .- centerY[l])) / minorAxis[l]) .^ 2 .< 1)
    end

    return P
end

shepp_logan(N::Int64; highContrast=true) = shepp_logan(N, N; highContrast=highContrast)


"""
    random_circles(M, N; n_circles=10)
    random_circles(N; n_circles=10)

Sum of `n_circles` random ellipses (random center, axes, orientation, gray level),
each contained in the unit disk, normalized so that `maximum(abs.(P)) == 1`.
Call `Random.seed!(...)` beforehand for reproducible images.
"""
function random_circles(M::Int64, N::Int64; n_circles::Int64=10)
    P = zeros(M, N)
    x = ((0:(N-1)) / div(N, 2) .- 1)'
    y = ((0:(M-1)) / div(M, 2) .- 1)

    for _ in 1:n_circles
        # center at distance R < 1 from the origin, in a uniformly random direction
        # (α is an integer in -180:180 used directly as radians, kept as in the original)
        R = rand()
        α = rand(-180:180)
        centerX = R * cos(α)
        centerY = R * sin(α)

        # Axes < 1 - R guarantee the ellipse stays inside the unit disk
        majorAxis = rand() * (1 - R)
        minorAxis = rand() * (1 - R)
        theta = rand(-180:180)           # orientation in degrees
        grayLevel = rand(-1:0.1:1)

        c = cos(theta / 360 * 2 * pi)
        s = sin(theta / 360 * 2 * pi)
        P += grayLevel * (
            ((c * (x .- centerX) .+ s * (y .- centerY)) / majorAxis) .^ 2 .+
            ((s * (x .- centerX) .- c * (y .- centerY)) / minorAxis) .^ 2 .< 1)
    end

    # guard against an all-zero image (all gray levels 0 or tiny axes)
    m = maximum(abs.(P))
    return m > 0 ? P ./ m : P
end

random_circles(N::Int64; n_circles::Int64=10) = random_circles(N, N; n_circles=n_circles)

end # module MyPhantomTestImg
