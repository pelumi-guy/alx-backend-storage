-- A SQL script that lists all bands with Glam rock as their main style, ranked by their longevity
SELECT band_name, 
	IFNULL(split, (
			SELECT EXTRACT(YEAR FROM CURDATE())
	) - 1) - formed AS lifespan
	FROM metal_bands
	WHERE style LIKE '%Glam rock%'
	ORDER BY lifespan DESC
