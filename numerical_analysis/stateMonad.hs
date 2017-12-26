-- module Main where
import Control.Monad.State

-- ステートモナドのメモ
-- 参照元：https://qiita.com/tsukimizake774/items/9c60c9e06ebc56b648b7#fnref2

-- type Work = Int
-- type Day  = Int
-- type WorkState = (Work,Day)
--
-- work :: State WorkState Work
-- work = do
--   -- 現在の状態を変数に束縛
--    (workLeft, daysLeft) <- get
--    print $runState work (workLeft, daysLeft)
--    let todaysWork = workLeft `div` daysLeft ^ 2
--    if daysLeft == 1
--      then return workLeft
--    else do
--      put  (workLeft - todaysWork, daysLeft - 1)
--      work
--
-- main :: IO ()
-- main = do
--   ws <- getLine
--   ds <- getLine
--   let w =  read ws :: Int
--   let d =  read ds :: Int
--   --runStateは Stateモナドからs->(a,s)型の関数を取り出し、s型の値を初期状態として実行
--   print $runState work (w, d)

type Stat = (Int,Integer,Integer)

fib_ :: Int -> Int
fib_ 0 = 0
fib_ 1 = 1
fib_ n = fib_ (n-1) + fib_ (n-2)

fib :: Int -> Integer
fib 0 = 0
fib 1 = 1
fib n = evalState fibImpl (2, 1, 0)
  where
    fibImpl :: State Stat Integer
    fibImpl = do
      (i, r1, r2) <- get
      if i == n
        then return $ r1 + r2
        else do
          put (i + 1, r1 + r2, r1)
          fibImpl

main :: IO()
main = print $ fib 10000
