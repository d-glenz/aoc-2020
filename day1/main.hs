
solution1 :: [Int] -> [(Int,Int,Int)]
solution1 expenses = [(a*b,a,b) | a <- expenses, b <- expenses, a+b == 2020]

solution2 :: [Int] -> [(Int,Int,Int,Int,Int)]
solution2 expenses = [(a*b*c,a+b+c,a,b,c) | a <- expenses, 
                                            b <- expenses,
                                            c <- expenses, a+b+c == 2020]

main = do
  file <- readFile "input1.test"
  let expenses = map (\x -> read x::Int) $ lines file
  print $ show $ solution1 expenses
  print $ show $ solution2 expenses
