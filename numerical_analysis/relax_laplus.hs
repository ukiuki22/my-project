--正方形領域で定義されたluplus方程式を緩和法で解く
import Data.Array.Repa as R

type Scalar t = R.Array t DIM2 Double


--n_x,yは境界込のサイズ
initial_solution :: (Int,Int) -> Scalar U
initial_solution (n_x,n_y) = computeS $fromFunction (Z:.n_x:.n_y) f0
  where f0 (Z:.i:.j) = 1.0

step :: (Int,Int) -> Scalar U -> IO (Scalar U)
step (n_x,n_y) f1 = do
  fP <- computeP $ fromFunction (Z:.n_x:.n_y) f2 
  return fP
  where 
--境界条件はコンデンサーの中のイメージ
    f2 (Z:.i:.j) 
      | i==  0   = 0
      | i==n_x-1 = fromIntegral(n_x-1)
      | j== 0 || j ==　n_y-1 = fromIntegral(i)
      | otherwise = ( f1!(Z:.i+1:.j)+f1!(Z:.i:.j+1)+f1!(Z:.i-1:.j)+f1!(Z:.i:.j-1) )/4

update :: (Int,Int) -> Int -> Int -> Scalar U -> IO()
update (n_x,n_y) num1 num2 f0 = do
  f1 <- step (n_x,n_y) f0
  print f1
  if (num1>0) then
    update (n_x,n_y) (num1-1) num2 f1
  else return ()

main :: IO()
main = do
  update (5,5) 50 1 $initial_solution (5,5)
