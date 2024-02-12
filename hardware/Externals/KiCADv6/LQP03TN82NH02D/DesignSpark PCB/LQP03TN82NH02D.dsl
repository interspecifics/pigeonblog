SamacSys ECAD Model
3446514/1236916/2.50/2/2/Inductor

DESIGNSPARK_INTERMEDIATE_ASCII

(asciiHeader
	(fileUnits MM)
)
(library Library_1
	(padStyleDef "r30_25"
		(holeDiam 0)
		(padShape (layerNumRef 1) (padShapeType Rect)  (shapeWidth 0.250) (shapeHeight 0.300))
		(padShape (layerNumRef 16) (padShapeType Ellipse)  (shapeWidth 0) (shapeHeight 0))
	)
	(textStyleDef "Default"
		(font
			(fontType Stroke)
			(fontFace "Helvetica")
			(fontHeight 50 mils)
			(strokeWidth 5 mils)
		)
	)
	(patternDef "LQP03TG3N1B02D" (originalName "LQP03TG3N1B02D")
		(multiLayer
			(pad (padNum 1) (padStyleRef r30_25) (pt -0.275, 0.000) (rotation 90))
			(pad (padNum 2) (padStyleRef r30_25) (pt 0.275, 0.000) (rotation 90))
		)
		(layerContents (layerNumRef 18)
			(attr "RefDes" "RefDes" (pt 0.000, 0.000) (textStyleRef "Default") (isVisible True))
		)
		(layerContents (layerNumRef 28)
			(line (pt -0.3 0.15) (pt 0.3 0.15) (width 0.1))
		)
		(layerContents (layerNumRef 28)
			(line (pt 0.3 0.15) (pt 0.3 -0.15) (width 0.1))
		)
		(layerContents (layerNumRef 28)
			(line (pt 0.3 -0.15) (pt -0.3 -0.15) (width 0.1))
		)
		(layerContents (layerNumRef 28)
			(line (pt -0.3 -0.15) (pt -0.3 0.15) (width 0.1))
		)
		(layerContents (layerNumRef 30)
			(line (pt -0.625 0.35) (pt 0.625 0.35) (width 0.1))
		)
		(layerContents (layerNumRef 30)
			(line (pt 0.625 0.35) (pt 0.625 -0.35) (width 0.1))
		)
		(layerContents (layerNumRef 30)
			(line (pt 0.625 -0.35) (pt -0.625 -0.35) (width 0.1))
		)
		(layerContents (layerNumRef 30)
			(line (pt -0.625 -0.35) (pt -0.625 0.35) (width 0.1))
		)
		(layerContents (layerNumRef 18)
			(line (pt 0 0.15) (pt 0 -0.15) (width 0.1))
		)
	)
	(symbolDef "LQP03TN82NH02D" (originalName "LQP03TN82NH02D")

		(pin (pinNum 1) (pt 0 mils 0 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName false)) (pinName (text (pt 0 mils -35 mils) (rotation 0]) (justify "UpperLeft") (textStyleRef "Default"))
		))
		(pin (pinNum 2) (pt 800 mils 0 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName false)) (pinName (text (pt 800 mils -35 mils) (rotation 0]) (justify "UpperRight") (textStyleRef "Default"))
		))
		(arc (pt 250 mils -2 mils) (radius 50 mils) (startAngle 177.7) (sweepAngle -175.4) (width 6 mils))
		(arc (pt 350 mils -2 mils) (radius 50 mils) (startAngle 177.7) (sweepAngle -175.4) (width 6 mils))
		(arc (pt 450 mils -2 mils) (radius 50 mils) (startAngle 177.7) (sweepAngle -175.4) (width 6 mils))
		(arc (pt 550 mils -2 mils) (radius 50 mils) (startAngle 177.7) (sweepAngle -175.4) (width 6 mils))
		(attr "RefDes" "RefDes" (pt 650 mils 250 mils) (justify Left) (isVisible True) (textStyleRef "Default"))

	)
	(compDef "LQP03TN82NH02D" (originalName "LQP03TN82NH02D") (compHeader (numPins 2) (numParts 1) (refDesPrefix L)
		)
		(compPin "1" (pinName "1") (partNum 1) (symPinNum 1) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(compPin "2" (pinName "2") (partNum 1) (symPinNum 2) (gateEq 0) (pinEq 0) (pinType Bidirectional))
		(attachedSymbol (partNum 1) (altType Normal) (symbolName "LQP03TN82NH02D"))
		(attachedPattern (patternNum 1) (patternName "LQP03TG3N1B02D")
			(numPads 2)
			(padPinMap
				(padNum 1) (compPinRef "1")
				(padNum 2) (compPinRef "2")
			)
		)
		(attr "Mouser Part Number" "")
		(attr "Mouser Price/Stock" "")
		(attr "Manufacturer_Name" "Murata Electronics")
		(attr "Manufacturer_Part_Number" "LQP03TN82NH02D")
		(attr "Description" "LQP03TN_02 Series Inductor 82nH +/-3% 0201 (0603)")
		(attr "Datasheet Link" "https://psearch.en.murata.com/inductor/product/LQP03TN82NH02%23.html")
		(attr "Height" "0.33 mm")
	)

)
